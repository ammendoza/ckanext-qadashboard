import ckan.authz as authz
import ckan.lib.base as base
import ckan.logic as logic
import ckan.model as model
import ckan.plugins.toolkit as toolkit
import ckanext.qadashboard.model as _model
import ckanext.qadashboard.util as _util

from ckan.common import _, request

c = toolkit.c
abort = base.abort

class ProblemController(toolkit.BaseController):

    def __call__(self, environ, start_response):

        # Check if user can read the package
        routes_dict = environ['pylons.routes_dict']
        
        if 'package_id' in routes_dict:
            context = {'model': model, 'session': model.Session,
                   'user': c.user, 'for_view': True,
                   'auth_user_obj': c.userobj}
            data_dict = {'id': routes_dict['package_id']}
            try:
                c.pkg_dict = logic.get_action('package_show')(context, data_dict)
                c.pkg = context['package']
                dataset_type = c.pkg_dict['type'] or 'dataset'
            except logic.NotFound:
                abort(404, _('Dataset not found'))
            except logic.NotAuthorized:
                    abort(403, _('Unauthorized to read dataset %s') % id)
        
        return toolkit.BaseController.__call__(self, environ, start_response)

    def view_dataset(self, package_id):
      
        problems = _model.Problem.by_package(package_id=c.pkg.id)

        return toolkit.render('package/problems.html', extra_vars={
                'problems': problems
            })
        
    def view_problem(self, id, package_id):
                
        problem_data = _model.Problem.get_related(id)
        problem_updates = _model.ProblemUpdate.by_problem(problem_id=id)

        return toolkit.render('package/problem_read.html', extra_vars={
                'problem': problem_data.Problem,
                'updates': problem_updates,
                'user': problem_data.User
            })
        
    def edit_problem(self, id, package_id, errors={}):

        problem = _model.Problem.get(id)
        problem_types = _model.ProblemType.all()

        return toolkit.render('package/problem_form.html', extra_vars={
                'package_id': package_id,
                'problem_types': problem_types,
                'problem': problem,
                'status': _model.Status.as_array(),
                'action' : 'edit',
                'errors': errors
            })
            
    def new_problem(self, package_id, errors = {}):

        problem = {}
        problem_types = _model.ProblemType.all()

        return toolkit.render('package/problem_form.html', extra_vars={
                'action': 'new',
                'problem': problem,
                'problem_types': problem_types,
                'errors': errors
            })
    
    def form_save(self, package_id):

        #Get common form parameters
        params = request.params
        action = params.get('action')
        package_id = params.get('package_id')
        title = params.get('title')
        problem_id = params.get('id')
        status = params.get('status')
        user_id = c.userobj.id
        description = params.get('description')
             
        errors = {}
        
        if action == 'new':
        
            if not title:
                errors['title'] = ['You must provide a title']
                
            if not description:
                errors['description'] = ['You must provide a description']
        
            if not errors:
                #Create new problem
                problem = _model.Problem(package_id=package_id, title=title, creator_id=user_id, problem_type=params.get('type'), description=description)
                model.Session.add(problem)
            
        else:

            #Update problem entity
            problem = _model.Problem.get(problem_id)
            
            if problem.current_status == status and not description:
            
                errors = {'msg': u'No changes made'}
            
            else:
                
                status_changed = False
                if problem.current_status != status:
                    status_changed = True
            
                problem.current_status = status
                
                #Create new problem update
                problem_update = _model.ProblemUpdate(problem_id=problem_id, 
                                    user_id=user_id, 
                                    status_id=status, 
                                    status_changed=status_changed, 
                                    notes=description)
                model.Session.add(problem_update)
            
        if len(errors) == 0:
            #Commit model changes
            model.Session.commit()

            toolkit.redirect_to('problem_detail', id=problem.id, package_id=package_id)
        
        else:
            if action == 'new':
                return self.new_problem(package_id, errors)
            else:
                return self.edit_problem(problem_id, package_id, errors)
                
        
    def dashboard(self):
    
        context = {'for_view': True, 'user': c.user,
                   'auth_user_obj': c.userobj}
        data_dict = {'user_obj': c.userobj, 'include_datasets': True}
        
        c.is_sysadmin = authz.is_sysadmin(c.user)
        try:
            user_dict = logic.get_action('user_show')(context, data_dict)
        except logic.NotFound:
            h.flash_error(_('Not authorized to see this page'))
            h.redirect_to(controller='user', action='login')
        except logic.NotAuthorized:
            abort(403, _('Not authorized to see this page'))
    
        if c.userobj.sysadmin:
        
            problems = _model.Problem.all()
        
        else:
            
            packages, package_ids = _util.get_user_packages()
            problems = _model.Problem.in_packages(package_ids)
            
        return toolkit.render('user/dashboard_problems.html', extra_vars={
                'user_dict': user_dict,
                'problems': problems
            })
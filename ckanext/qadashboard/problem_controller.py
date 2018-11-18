import ckan.lib.base as base
import ckan.logic as logic
import ckan.model as model
import ckan.plugins.toolkit as toolkit
import ckanext.qadashboard.model as _model

from ckan.common import _, request

c = toolkit.c
abort = base.abort

class ProblemController(toolkit.BaseController):

    def view_dataset(self, id):
    
        context = {'model': model, 'session': model.Session,
                   'user': c.user, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id}
        try:
            c.pkg_dict = logic.get_action('package_show')(context, data_dict)
            c.pkg = context['package']
            '''c.package_activity_stream = get_action(
                'package_activity_list_html')(
                context, {'id': c.pkg_dict['id']})'''
            dataset_type = c.pkg_dict['type'] or 'dataset'
        except logic.NotFound:
            abort(404, _('Dataset not found'))
        except logic.NotAuthorized:
                abort(403, _('Unauthorized to read dataset %s') % id)
                
        problems = _model.Problem.by_package(package_id=c.pkg.id)

        return toolkit.render('package/problems.html', extra_vars={
            'problems': problems
        })
        
    def view_problem(self, id, package_id):
    
        print 'view_problem'
    
        context = {'model': model, 'session': model.Session,
                   'user': c.user, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': package_id}
        try:
            c.pkg_dict = logic.get_action('package_show')(context, data_dict)
            c.pkg = context['package']
            '''c.package_activity_stream = get_action(
                'package_activity_list_html')(
                context, {'id': c.pkg_dict['id']})'''
            dataset_type = c.pkg_dict['type'] or 'dataset'
        except logic.NotFound:
            abort(404, _('Dataset not found'))
        except logic.NotAuthorized:
                abort(403, _('Unauthorized to read dataset %s') % package_id)
                
        problem_data = _model.Problem.get_related(id)

        return toolkit.render('package/problem_read.html', extra_vars={
                'problem': problem_data.Problem,
                'user': problem_data.User
            })
        
    def edit_problem(self, id, package_id):
    
        context = {'model': model, 'session': model.Session,
                   'user': c.user, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': package_id}
        try:
            c.pkg_dict = logic.get_action('package_show')(context, data_dict)
            c.pkg = context['package']
            '''c.package_activity_stream = get_action(
                'package_activity_list_html')(
                context, {'id': c.pkg_dict['id']})'''
            dataset_type = c.pkg_dict['type'] or 'dataset'
        except logic.NotFound:
            abort(404, _('Dataset not found'))
        except logic.NotAuthorized:
                abort(403, _('Unauthorized to read dataset %s') % package_id)
                
        errors = {}
        problem_data = _model.Problem.get(id)
        problem_types = _model.ProblemType.all()

        return toolkit.render('package/problem_form.html', extra_vars={
                'package_id': package_id,
                'problem_types': problem_types,
                'problem': problem_data.Problem,
                'action' : 'edit',
                'errors': errors
            })
            
    def new_problem(self, id, package_id):
    
        context = {'model': model, 'session': model.Session,
                   'user': c.user, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': package_id}
        try:
            c.pkg_dict = logic.get_action('package_show')(context, data_dict)
            c.pkg = context['package']
            '''c.package_activity_stream = get_action(
                'package_activity_list_html')(
                context, {'id': c.pkg_dict['id']})'''
            dataset_type = c.pkg_dict['type'] or 'dataset'
        except logic.NotFound:
            abort(404, _('Dataset not found'))
        except logic.NotAuthorized:
                abort(403, _('Unauthorized to read dataset %s') % package_id)
             
        problem = {}
        errors = {}

        return toolkit.render('package/problem_form.html', extra_vars={
                'action': 'new',
                'problem': problem,
                'errors': errors
            })
    
    def form_save(self, package_id):
    
        context = {'model': model, 'session': model.Session,
                   'user': c.user, 'for_view': True,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': package_id}
        
        print 'save_form'
        
        try:
            c.pkg_dict = logic.get_action('package_show')(context, data_dict)
            c.pkg = context['package']
            dataset_type = c.pkg_dict['type'] or 'dataset'
        except logic.NotFound:
            abort(404, _('Dataset not found'))
        except logic.NotAuthorized:
                abort(403, _('Unauthorized to read dataset %s') % package_id)
                
        params = request.params
        action = params.get('action')
             
        errors = {}
        if action == 'new':
            problem = _model.Problem(package_id=params.get('package_id'), creator_id=c.userobj.id, problem_type=params.get('type'), description=params.get('description'))
            model.Session.add(problem)
            model.Session.commit()
        else:
            problem = _model.Problem.get(params.get('id'))
        
        return toolkit.render('package/problem_form.html', extra_vars={
                'problem': problem,
                'errors': errors
            })
            
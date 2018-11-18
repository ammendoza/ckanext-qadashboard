import ckan.logic as logic
import ckan.model as model
import ckan.plugins.toolkit as toolkit

c = toolkit.c


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

        return toolkit.render('package/problems.html', extra_vars={})
        
    def view_problem(self, id, package_id):
    
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

        return toolkit.render('package/problem_read.html', extra_vars={})
        
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

        return toolkit.render('package/problem_form.html', extra_vars={})
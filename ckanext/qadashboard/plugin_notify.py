import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class NotifyProblemsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'qadashboard')

    def before_map(self, map):
        map.connect(
            '/dashboard/qa',
            controller='ckanext.qadashboard.db_controller:DashboardController',
            action='view'
        )
        
        map.connect(
            'dataset_problems', 
            '/dataset/problems/{package_id}',
            controller='ckanext.qadashboard.problem_controller:ProblemController',
            action='view_dataset'
        )
        
        map.connect(
            'problem_detail', 
            '/dataset/problems/{package_id}/view/{id}',
            controller='ckanext.qadashboard.problem_controller:ProblemController',
            action='view_problem'
        )
        
        map.connect(
            'problem_edit', 
            '/dataset/problems/{package_id}/edit/{id}',
            controller='ckanext.qadashboard.problem_controller:ProblemController',
            action='edit_problem'
        )
        
        map.connect(
            'problem_save', 
            '/dataset/problems/{package_id}/save',
            controller='ckanext.qadashboard.problem_controller:ProblemController',
            action='form_save'
        )
        
        return map
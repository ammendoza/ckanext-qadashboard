import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class QadashboardPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'qa-dashboard')
        
    def before_map(self, map):
        map.connect(
            '/dashboard/qa',
            controller='ckanext.qadashboard.db_controller:DashboardController',
            action='view'
        )
        
        map.connect(
            'dataset_problems', 
            '/dataset/problems/{id}',
            controller='ckanext.qadashboard.problem_controller:ProblemController',
            action='view_dataset'
        )
        
        map.connect(
            'problem_detail', 
            '/dataset/problems/{package_id}/{id}',
            controller='ckanext.qadashboard.problem_controller:ProblemController',
            action='view_problem'
        )
        
        map.connect(
            'problem_edit', 
            '/dataset/problems/{package_id}/edit/{id}',
            controller='ckanext.qadashboard.problem_controller:ProblemController',
            action='edit_problem'
        )
        
        return map
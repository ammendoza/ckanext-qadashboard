import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class QadashboardPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates/qadashboard')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'qa-dashboard')
        
    def before_map(self, map):

        map.connect(
            'dashboard.qa',
            '/dashboard/qa',
            controller='ckanext.qadashboard.db_controller:DashboardController',
            action='view'
        )
        
        return map
import ckan.plugins.toolkit as toolkit

c = toolkit.c


class DashboardController(toolkit.BaseController):

    def view(self):
    
    
        return toolkit.render('qadashboard/index.html', extra_vars={})
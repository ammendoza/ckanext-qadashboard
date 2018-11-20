import ckan.authz as authz
import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.logic as logic
import ckan.model as model
import ckan.plugins.toolkit as toolkit
import ckanext.qadashboard.model as _model

import ast
import pprint

from ckan.common import _, c, request
from datetime import date, timedelta
from decimal import Decimal

class DashboardController(toolkit.BaseController):

    def __before__(self, action, **env):
        toolkit.BaseController.__before__(self, action, **env)
        try:
            context = {'model': model, 'user': c.user,
                       'auth_user_obj': c.userobj}
            toolkit.check_access('site_read', context)
        except logic.NotAuthorized:
            if c.action not in ('login', 'request_reset', 'perform_reset',):
                abort(403, _('Not authorized to see this page'))

    def view(self):      
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

        c.user_dict = user_dict
        c.is_myself = user_dict['name'] == c.user
        c.about_formatted = h.render_markdown(user_dict['about'])
             
        #Initialize variables
        packages = []
        problems = []
        views = []
        averages = {
            'problem_total': 0,
            'problem_average': 0.0,
            'my_problem_total': 0,
            'my_problem_average': 0.0,
            'qa_average': 0,
            'my_qa_total': 0,
            'my_qa_average': 0.0,
            'views_total': 0,
            'views_average': 0.0,
            'my_views_total': 0,
            'my_views_average': 0.0,
            'total_packages': 0,
            'show_comparison': True
            }
        
            
        #Get values for all packages
        packages = toolkit.get_action('package_search')(context, {
                    'include_private': True,
                    'rows': 1000,
                    'sort': 'name asc'
                })
        
        if 'count' in packages:
                averages['total_packages'] = packages['count']
                
        if 'results' in packages:
            packages = packages['results']

        #Get qa values for all packages
        qa_levels, low_qa, averages['qa_total'] = self.__get_qa_values(packages)
            
        #Get problem total for all datasets
        problems = _model.Problem.open()
        averages['problem_total'] = len(problems)
        
        #Get last week start and end date
        day_count = 7
        today = date.today()
        start_date = today - timedelta(days=day_count+1)
        end_date = today - timedelta(days=1)
        
        #Get views by date
        db_views = _model.TrackingSummary.get_by_date(start_date, end_date)
        
        for view in db_views:
            averages['views_total'] += view[1]
    
        if c.userobj.sysadmin:
        
            averages['show_comparison'] = False
            averages['my_qa_total'] = averages['qa_total']
            averages['my_views_total'] = averages['views_total']
            averages['my_problem_total'] = averages['problem_total']
        
        else:
        
            #Regular users can only edit packages for groups that they are authorized for
            user_groups = toolkit.get_action('group_list_authz')(context, {})
            group_search = ''
            
            if user_groups:
                for group in user_groups:
                    if group != '':
                        group_search = group_search + ' OR '
                    group_search = group_search + group['name']
                    
                packages = toolkit.get_action('package_search')(context, {
                        'fq': 'group:('+ group_search +')',
                        'include_private': True,
                        'rows': 1000,
                        'sort': 'name asc'
                    })
                
                if 'results' in packages:
                    packages = packages['results']
                    
                    #Get last 5 problems for datasets that the user can edit
                    package_ids = []
                    for package in packages:
                        package_ids.append(package['id'])

                    problems = _model.Problem.in_packages(package_ids)
                    averages['my_problem_total'] = len(problems)
            
                    #Get qa values for my packages
                    qa_levels, low_qa, my_qa_total = self.__get_qa_values(packages)
        
        if packages:
            #Order packages by their QA to get the 5 lowest
            low_qa = sorted(low_qa, key=lambda k: k['level'], reverse=True)
            
            #Get averages
            if (averages['qa_total'] > 0):
                averages['qa_average'] = round(averages['qa_total'] / float(averages['total_packages']), 2)
                    
            if (averages['views_total'] > 0):
                averages['views_average'] = round(averages['views_total'] / float(averages['total_packages']), 2)
            
            if (averages['problem_total'] > 0):
                averages['problem_average'] = round(averages['problem_total'] / float(averages['total_packages']), 2)
                
            if (averages['my_qa_total'] > 0):
                averages['my_qa_average'] = round(averages['my_qa_total'] / float(len(packages)), 2)
                
            if (averages['my_views_total'] > 0):
                averages['my_views_average'] = round(averages['my_views_total'] / float(len(packages)), 2)

            if (averages['my_problem_total'] > 0):
                averages['my_problem_average'] = round(averages['my_problem_total'] / float(len(packages)), 2)
                    
        #Fill dates with no views in order to print zero values
        last_index = 0
        for aux_date in (start_date + timedelta(n) for n in range(day_count)):
        
            data = 0
            for idx, db_view in enumerate(db_views[last_index:]):

                if db_views[last_index + idx][0] == aux_date:
                    data = db_views[last_index + idx][1]
                    last_index = last_index + idx + 1
                    break
            
            views.append({
                    'label': aux_date,
                    'data': data,
                })

    
        #Render page
        return toolkit.render('user/dashboard_qa.html', extra_vars={
                'user_dict': user_dict,
                'problem_list': problems[:5],
                'qa_levels': qa_levels,
                'low_qa': low_qa[:5],
                'views': views,
                'averages': averages
            })

    @staticmethod
    def __get_qa_values (packages):
    
        qa_levels = []
        low_qa = []
        qa_total = 0
        
        for i in range(0,5):
            qa_levels.append(0)
    
        for package in packages:
            max_qa = -1
            if 'resources' in package:
                for resource in package['resources']:
                    if 'qa' in resource:
                        qa = ast.literal_eval(resource['qa'])
                        if qa['openness_score'] > max_qa:
                            max_qa = int(qa['openness_score'])
            
            if max_qa > -1:
                qa_levels[max_qa] += 1
                qa_total += max_qa
                
                #If qa level is lower than 3, save to low quality array
                if max_qa <= 3:
                    low_qa.append({
                            'level': max_qa,
                            'package': package
                        })
                        
        return qa_levels, low_qa, qa_total
import ckan.lib.base as base
import ckan.logic as logic
import ckan.model as model
import ckan.plugins.toolkit as toolkit
import ckanext.qadashboard.model as _model

import ast
import pprint

from ckan.common import _, request

c = toolkit.c

class DashboardController(toolkit.BaseController):

    def view(self):
        context = {'model': model, 'session': model.Session,
                    'user': c.user, 'for_view': True,
                    'auth_user_obj': c.userobj}
             
        #Initialize variables
        packages = []
        problems = []
        qa_levels = []
        low_qa = []
        problem_total = 0
        problem_average = 0
        my_problem_total = 0
        my_problem_average = 0
        qa_total = 0
        qa_average = 0
        my_qa_total = 0
        my_qa_average = 0
        views_total = 0
        views_average = 0
        my_views_total = 0
        my_views_average = 0
        total_packages = 0
        
        for i in range(0,5):
            qa_levels.append(0)
            
        #Get problem total for all datasets
        problems = _model.Problem.open()
        problem_total = len(problems)
    
        if c.userobj.sysadmin:
        
            #Sysadmin can edit all packages
            packages = toolkit.get_action('package_search')(context, {
                    'include_private': True,
                    'rows': 1000,
                    'sort': 'name asc'
                })
                
            if 'results' in packages:
                packages = packages['results']
                
            my_problem_total = len(problems)

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
                    my_problem_total = len(problems)
            
            #Get the number of total packages in the catalogue
            total_packages = toolkit.get_action('package_search')(context, {
                    'include_private': True,
                    'rows': 0
                })
                
            if 'count' in total_packages:
                total_packages = total_packages['count']
                
        #Get quality levels
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
                my_qa_total += max_qa
                
                #If qa level is lower than 3, save to low quality array
                if max_qa <= 3:
                    low_qa.append({
                            'level': max_qa,
                            'package': package
                        })
        if packages:
            #Order packages by their QA to get the 5 lowest
            low_qa = sorted(low_qa, key=lambda k: k['level'], reverse=True)
            
            #Get averages
            if (my_qa_total > 0):
                my_qa_average = my_qa_total / len(packages)
                
            if (my_views_total > 0):
                my_views_average = my_views_total / len(packages)

            if (my_problem_total > 0):
                my_problem_average = my_problem_total / len(packages)
            
            if (total_packages > 0):
                if (qa_total > 0):
                    qa_average = qa_total / total_packages
                    
                if (views_total > 0):
                    views_average = views_total / total_packages
                
                if (problem_total > 0):
                    problem_average = problem_total / total_packages

    
        return toolkit.render('qadashboard/index.html', extra_vars={
                'problem_list': problems[:5],
                'qa_levels': qa_levels,
                'low_qa': low_qa[:5],
                'my_qa_average': my_qa_average,
                'qa_average': qa_average,
                'my_views_average': my_views_average,
                'views_average': views_average,
                'my_problem_average': my_problem_average,
                'problem_average': problem_average
            })
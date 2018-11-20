import ckan.model as model
import ckan.plugins.toolkit as toolkit

from ckan.common import c

def get_user_packages ():

    context = {'model': model, 'user': c.user,
                'auth_user_obj': c.userobj}

    packages = []
    package_ids = []
    user_groups = toolkit.get_action('group_list_authz')(context, {})
    group_search = ''
    
    if user_groups:
        for group in user_groups:
            if group_search != '':
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
        
            for package in packages:
                package_ids.append(package['id'])
            
    return packages, package_ids
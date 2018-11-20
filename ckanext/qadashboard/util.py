import ckan.model as model
import ckan.plugins.toolkit as toolkit
import pprint

from ckan.common import c

def get_user_packages ():

    context = {'model': model, 'user': c.user,
                'auth_user_obj': c.userobj}

    packages = []
    package_ids = []
    user_organization = toolkit.get_action('organization_list_for_user')(context, {
					'permission': 'create_dataset'
                })
    
    organization_search = ''
    
    if user_organization:
        for organization in user_organization:
            if organization_search != '':
                organization_search = organization_search + ' OR '
            organization_search = organization_search + organization['name']
            
        packages = toolkit.get_action('package_search')(context, {
                'fq': 'organization:('+ organization_search +')',
                'include_private': True,
                'rows': 1000,
                'sort': 'name asc'
            })

        if 'results' in packages:
            packages = packages['results']
        
            for package in packages:
                package_ids.append(package['id'])
            
    return packages, package_ids
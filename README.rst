=============
ckanext-qadashboard
=============

``ckanext-qadashboard`` enables a QA based user dashboard and a problem notification system for datasets. This extension contains two plugins:

- **qadashboard**: enables a QA user dashboard showing basic information about user's datasets (qa levels, lowest rated datasets, last added problems, last week views and dataset/site average values).
- **notifyproblems**: enables the problem notification subsystem and adds a "Problems" menu option for each dataset and to the user dashboard.

------------
Requirements
------------

This extension has been tested with CKAN 2.8 only.
It requires that the page view tracking CKAN feature is enabled and that the following CKAN extensions are installed and enabled along with their requirements:

- ckanext-qa: https://github.com/ckan/ckanext-qa


------------
Installation
------------

To install ckanext-qadashboard:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the project in your main ckan folder, usually ``/etc/ckan/default/src/``:

     git clone https://github.com/ammendoza/ckanext-qadashboard.git
	 
3. Initialize the required database tables by running the following command:

     paster --plugin=ckanext-qadashboard qadashboard initdb --config=/etc/ckan/default/production.ini

4. Add ``qadashboard`` and ``notifyproblems`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

5. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


---------------
Config Settings
---------------

This extension does not have any additional configuration settings.

---------------
License
---------------

This extension is published under the GNU Affero General Public License v3 (see LICENSE).


=============
ckanext-qadashboard
=============

``ckanext-qadashboard`` enables a QA based user dashboard and a problem notification system for datasets. 

Plugins
------------
This extension contains two plugins, **qadashboard** and **notifyproblems**. 

Both make use of the model implemented with SQLAlchemy that can be found in the ``model.py`` file and the ``commands.py`` commands controller that creates the tables for the model.
The ``utils.py`` file contains methods that are common to both plugins, such as obtaining the list of datasets that the current user can edit.

------------
qadashboard
------------

Enables a QA user dashboard showing basic information about user's datasets (qa levels, lowest rated datasets, last added problems, last week views and dataset/site average values).

The plugin main class is ``plugin.py`` and its controller class is ``qa_controller.py``. Its template files can be found under ``templates/qadashboard``.

Chart.js 2.7.3 is included through a CDN in order to show the openness score and last week views charts.

------------
notifyproblems
------------

Enables the problem notification subsystem and adds a "Problems" menu option for each dataset and to the user dashboard.

The plugin main class is ``plugin_notify.py`` and its controller class is ``problem_controller.py``. Its template files can be found under ``templates/notifyproblems``.


Requirements
------------

This extension has been tested with CKAN 2.8 only.
It requires that the page view tracking CKAN feature is enabled and that the following CKAN extensions are installed and enabled along with their requirements:

- ckanext-qa: https://github.com/ckan/ckanext-qa



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


Config Settings
---------------

This extension does not have any additional configuration settings.


How to use
------------

Once installed and enabled, navigate to the user dashboard in order to view the QA Dashboard:

.. image:: https://github.com/ammendoza/ckanext-qadashboard/raw/master/img/qa-dashboard.jpg

Problems reported for datasets which the current user can edit can be viewed from the "Problems" tab:

.. image:: https://github.com/ammendoza/ckanext-qadashboard/raw/master/img/qa-dashboard-problems.png

All users can view problems reported on a dataset from the "Problems" tab at the dataset detail page. From this tab, logged in users can also add a new problem for the dataset by clicking "Add problem".

.. image:: https://github.com/ammendoza/ckanext-qadashboard/raw/master/img/dataset-problems.jpg
 
The problem detail page shows all information about the problem added and user updates. Logged in users can add updates by clicking the "Update problem" button, but only users with permissions to edit the dataset can change problem's status.

.. image:: https://github.com/ammendoza/ckanext-qadashboard/raw/master/img/problem-detail.jpg

License
---------------

This extension is published under the GNU Affero General Public License v3 (see LICENSE).


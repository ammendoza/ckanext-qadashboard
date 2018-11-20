=============
ckanext-qadashboard
=============

.. Put a description of your extension here:
   What does it do? What features does it have?
   Consider including some screenshots or embedding a video!


------------
Requirements
------------

This extension has been tested with CKAN 2.8 only.


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

4. Add ``qadashboard`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

5. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


---------------
Config Settings
---------------

This extension does not have any additional configuration settings.


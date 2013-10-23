Django History
============

A reusable Django app showing the history of object based events. This is also "known" as timeline.  

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-history

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/arteria/django-history.git#egg=history

TODO: Describe further installation steps (edit / remove the examples below):

In settings.py add ``history`` to your ``INSTALLED_APPS`` and define ``HISTORY_DISPLAY_TYPES``.

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'history',
    )
    
    HISTORY_DISPLAY_TYPES = () 
    # Example: 
    # HISTORY_DISPLAY_TYPES = (('history/hello_world.html', 'Hello World'), 
    #                          ('history/hello_user.html',  'Hello User'), 
    #                         )
	
	
Add the ``history`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^history/', include('history.urls')),
    )

Before your tags/filters are available in your templates, load them by using

.. code-block:: html

	{% load history_tags %}


Don't forget to migrate your database

.. code-block:: bash

    ./manage.py syncdb


Usage
-----

Follow these steps to set up your history (timeline).

+ Create templates in history/<template name>.html and register the 
+ .. templates in ``HISTORY_DISPLAY_TYPES`` defined in your project settings.



History event rendering
~~~~~~~~~~~~~~~~~~~~~~~
The objects is passed as ``obj`` to the template defined in ``HISTORY_DISPLAY_TYPES``. In our "Hello User" template (history/hello_user.html), it's possible to access to the user's username by using ``{{ obj.username }}``. 

TODO
----

+ Potect private timelines
+ Allow sticky events (highlight, keep them on top)
+ moments.js https://github.com/moment/moment/
+ AJAX loading of next page
+ 

License
-------

Django History is brought to you with the MIT License (MIT).

Contribute
----------

If you want to contribute to this project, the best way is to send a pull request. Thanks in advance.

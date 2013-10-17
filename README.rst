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

    pip install -e git+git://github.com/mbrochh/django-reusable-app-template.git#egg=history

TODO: Describe further installation steps (edit / remove the examples below):

In settings.py add ``history`` to your ``INSTALLED_APPS`` and define ``HISTORY_DISPLAY_TYPES``.

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'history',
    )
    
    HISTORY_DISPLAY_TYPES = () 

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

TODO: Describe usage or point to docs. Also describe available settings and
templatetags.


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-history
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch

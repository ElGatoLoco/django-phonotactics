=====
Phonotactic Probability Calculator for Serbian Language
=====

Phonotactic Probability Calculator is a Django app for calculating phonotactic probabilities in Serbian language.


Quick start
-----------

PREREQUISITES:

- Django 1.10
- Django “form tools” app

-----------

0. Install prerequisites and the phonotactics app with pip::
	
	pip install django django-formtools django-phonotactics


1. Add prerequisites and "phonotactics" app to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'formtools',
        'phonotactics',
    ]

2. Include the phonotactics URLconf in your project urls.py like this::

    url(r'^', include('phonotactics.urls')),

3. Run `python manage.py migrate` to create the phonotactics models.

4. Run `python manage.py loaddata words.json` to load the basic corpus.

Django Email as Username
========================

**User authentication with email addresses instead of usernames.**

**Author:** Tom Christie, [@_tomchristie][1].

**See also:** [django-email-login][2], [django-email-usernames][3].


Overview
========

Allows you to treat users as having only email addresses, instead of usernames.

1. Provides an email auth backend and helper functions for creating users.
2. Patches the Django admin to handle email based user authentication.
3. Overides the `createsuperuser` command to create users with email only.
4. Treats email authentication as case-insensitive.


Requirements
============

Known to work with Django >= 1.3


Installation
============

Install from PyPI:

    pip install django-email-as-username

Add 'emailusernames' to INSTALLED_APPS.
Make sure to include it further down the list than 'django.contrib.auth'.

    INSTALLED_APPS = (
        ...
        'emailusernames',
    )

Set `EmailAuthBackend` as your authentication backend:

    AUTHENTICATION_BACKENDS = (
        'emailusernames.backends.EmailAuthBackend',
    )


Usage
=====

Creating users
--------------

You should create users using the `create_user` and `create_superuser`
functions.

    from emailusernames.utils import create_user, create_superuser

    create_user('me@example.com', 'password')
    create_superuser('admin@example.com', 'password')

Retrieving users
----------------

You can retrieve users, using case-insensitive email matching, with the
`get_user` function.  Similarly you can use `user_exists` to test if a given
user exists.

    from emailusernames.utils import get_user, user_exists

    user = get_user('someone@example.com')
    ...

    if user_exists('someone@example.com'):
        ...

Both functions also take an optional queryset argument if you want to filter
the set of users to retrieve.

    user = get_user('someone@example.com',
                    queryset=User.objects.filter('profile__deleted=False'))

Updating users
--------------

You can update a user's email and save the instance, without having to also 
modify the username.

    user.email = 'other@example.com'
    user.save()

Note that the `user.username` attribute will always return the email address, 
but behind the scenes it will be stored as a hashed version of the user's email.

Authenticating users
--------------------

You should use `email` and `password` keyword args in calls to `authenticate`,
rather than the usual `username` and `password`.

    from django.contrib.auth import authenticate
    
    user = authenticate(email='someone@example.com', password='password')
    if user:
        ...
    else:
        ...

User Forms
----------

`emailusernames` provides the following forms that you can use for 
authenticating, creating and updating users:

* `emailusernames.forms.EmailAuthenticationForm`
* `emailusernames.forms.EmailAdminAuthenticationForm`
* `emailusernames.forms.EmailUserCreationForm`
* `emailusernames.forms.EmailUserChangeForm`

Using Django's built-in login view
----------------------------------

If you're using `django.contrib.auth.views.login` in your urlconf, you'll want
to make sure you pass through `EmailAuthenticationForm` as an argument to
the view.

    from emailusernames.forms import EmailAuthenticationForm

    urlpatterns = patterns('',
        ...
        url(r'^auth/login$', 'django.contrib.auth.views.login',
            {'authentication_form': EmailAuthenticationForm}, name='login'),
        ...
    )


Management commands
===================

`emailusernames` will patch up the `syncdb` and `createsuperuser` managment
commands, to ensure that they take email usernames.

    bash: ./manage.py syncdb
    ...
    You just installed Django's auth system, which means you don't have any superusers defined.
    Would you like to create one now? (yes/no): yes
    E-mail address:


Migrating existing projects
===========================

`emailusernames` includes a function you can use to easily migrate existing
projects.

The migration will refuse to run if there are any users that it cannot migrate
either because they do not have an email set, or because there exists a
duplicate email for more than one user.

There are two ways you might choose to run this migration.

Run the update manually
-----------------------

Using `manage.py shell`:

    bash: python ./manage.py shell
    >>> from emailusernames.utils import migrate_usernames
    >>> migrate_usernames()
    Successfully migrated usernames for all 12 users

Run as a data migration
-----------------------

Using `south`, and assuming you have an app named `accounts`, this might look
something like:

    bash: python ./manage.py datamigration accounts email_usernames
    Created 0002_email_usernames.py.

Now edit `0002_email_usernames.py`:

    from emailusernames.utils import migrate_usernames

    def forwards(self, orm):
        "Write your forwards methods here."
        migrate_usernames()

And finally apply the migration:

	python ./manage.py migrate accounts


Running the tests
=================

If you have cloned the source repo, you can run the tests using the
provided `manage.py`:

    ./manage.py test

Note that this application (unsurprisingly) breaks the existing
`django.contrib.auth` tests.  If your test suite currently includes those
tests you'll need to find a way to explicitly disable them.

Changelog
=========

1.4.6
-----

* EmailAuthenticationForm takes request as first argument, same as Django's
  AuthenticationForm.  Now fixed so it won't break if you didn't specify
  data as a kwarg.

1.4.5
-----

* Email form max lengths should be 75 chars, not 70 chars.
* Use `get_static_prefix` (Supports 1.3 and 1.4.), not `admin_media_prefix`.

1.4.4
-----

* Add 'queryset' argument to `get_user`, `user_exists`

1.4.3
-----

* Fix support for loading users from fixtures.
  (Monkeypatch `User.save_base`, not `User.save`)

1.4.2
-----

* Fix support for Django 1.4

1.4.1
-----

* Fix bug with displaying usernames correctly if migration fails

1.4.0
-----

* Easier migrations, using `migrate_usernames()`

1.3.1
-----

* Authentication backend now sets `User.backend`.

1.3.0
-----

* Use hashed username lookups for performance.
* Use Django's email regex validator, rather than providing our own version.
* Tweaks to admin.
* Tweaks to documentation and notes on upgrading. 

1.2.0
-----

* Fix import bug in `createsuperuser` managment command.

1.1.0
-----

* Fix bug in EmailAuthenticationForm

1.0.0
-----

* Initial release

License
=======

Copyright © 2012, DabApps.

All rights reserved.

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this 
list of conditions and the following disclaimer in the documentation and/or 
other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

[1]: http://twitter.com/_tomchristie
[2]: https://bitbucket.org/tino/django-email-login
[3]: https://bitbucket.org/hakanw/django-email-usernames

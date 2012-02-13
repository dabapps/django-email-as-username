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

Installation
============

Install from PyPI:

    pip install django-email-as-username

Add 'emailusernames' to INSTALLED_APPS.

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

If you're using `django.contrib.auth.views.login` in your urlconf, you'll want to
make sure you pass through `EmailAuthenticationForm` as an argument to the view.

    urlpatterns = patterns('',
        ...
        url(r'^auth/login$', 'django.contrib.auth.views.login',
            {'authentication_form': EmailAuthenticationForm}, name='login'),
        ...
    )

Upgrading
=========

Once you have implemented emails as usernames, you're ready to convert any
existing users.

First, in order to modify the original usernames, temporarily remove the
'emailusernames' app from `settings.INSTALLED_APPS`:

    INSTALLED_APPS = (
        ...
        #'emailusernames',
    )

You will need to restart your Django instance to activate this change.

Then, within the Django project's environment (e.g., in `python manage.py
shell`, run this code:

    from django.db                  import IntegrityError, transaction
    from django.conf                import settings
    from django.contrib.auth.models import User
    from emailusernames.utils       import _email_to_username

    # Print a nice header.

    title   = 'Upgrading: No More Usernames!'
    border  = len(title) + 2

    print('')
    print('=' * border)
    print('%s' % title)

    # Upgrade database.

    tot    = User.objects.count()
    failed = 0

    for user in User.objects.all():
        user.username = _email_to_username(user.email)
        try:
            sid = transaction.savepoint()
            user.save()
            transaction.savepoint_commit(sid)
        except IntegrityError:
            failed += 1
            print(
                "Could not convert user with username '%s' because the email "
                "<%s> is already taken." % (user.username, user.email)
            )
            transaction.savepoint_rollback(sid)

    print("Converted %d of %d users (%d failed)." % (tot - failed, tot, failed))
    print('=' * border)

If any user shares an email address with another user, it cannot be converted
as usernames must be unique. This script will convert as many as possible and
any other users that cannot be converted will be printed.

Finally, re-enable the 'emailusernames' app by uncommenting the line in
`settings.INSTALLED_APPS`:

    INSTALLED_APPS = (
        ...
        'emailusernames',
    )

Don't forget to restart your Django instance again!

Changelog
=========

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

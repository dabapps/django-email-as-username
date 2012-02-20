import base64
import hashlib
import os
import sys

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction


# We need to convert emails to hashed versions when we store them in the
# username field.  We can't just store them directly, or we'd be limited
# to Django's username <= 30 chars limit, which is really too small for
# arbitrary emails.
def _email_to_username(email):
    email = email.lower()  # Emails should be case-insensitive unique
    return base64.urlsafe_b64encode(hashlib.sha256(email).digest())[:30]


def get_user(email):
    """
    Return the user with given email address.
    Note that email address matches are case-insensitive.
    """
    return User.objects.get(username=_email_to_username(email))


def user_exists(email):
    """
    Return True if a user with given email address exists.
    Note that email address matches are case-insensitive.
    """
    try:
        get_user(email)
    except User.DoesNotExist:
        return False
    return True


def create_user(email, password=None, is_staff=None, is_active=None):
    """
    Create a new user with the given email.
    Use this instead of `User.objects.create_user`.
    """
    try:
        user = User.objects.create_user(None, email, password)
    except IntegrityError, err:
        if err.message == 'column username is not unique':
            raise IntegrityError('user email is not unique')
        raise

    if is_active is not None or is_staff is not None:
        if is_active is not None:
            user.is_active = is_active
        if is_staff is not None:
            user.is_staff = is_staff
        user.save()
    return user


def create_superuser(email, password):
    """
    Create a new superuser with the given email.
    Use this instead of `User.objects.create_superuser`.
    """
    return User.objects.create_superuser(None, email, password)


def migrate_usernames(stream=None, quiet=False):
    """
    Migrate all existing users to django-email-as-username hashed usernames.
    If any users cannot be migrated an exception will be raised and the
    migration will not run.
    """
    stream = stream or (quiet and open(os.devnull, 'w') or sys.stdout)

    # Check all users can be migrated before applying migration
    emails = set()
    errors = []
    for user in User.objects.all():
        if not user.email:
            errors.append("Cannot convert user '%s' because email is not "
                          "set." % (user.username, ))
        elif user.email.lower() in emails:
            errors.append("Cannot convert user '%s' because email '%s' "
                          "already exists." % (user.username, user.email))
        else:
            emails.add(user.email.lower())

    # Cannot migrate.
    if errors:
        [stream.write(error + '\n') for error in errors]
        raise Exception('django-email-as-username migration failed.')

    # Can migrate just fine.
    total = User.objects.count()
    for user in User.objects.all():
        user.save()

    stream.write("Successfully migrated usernames for all %d users\n"
                 % (total, ))

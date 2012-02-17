from django.contrib.auth.models import User
from emailusernames.utils import get_user


class EmailAuthBackend(object):

    """Allow users to log in with their email address"""

    supports_inactive_user = False
    supports_anonymous_user = False
    supports_object_permissions = False

    def authenticate(self, email=None, password=None):
        try:
            user = get_user(email)
            if user.check_password(password):
                user.backend = "%s.%s" % (self.__module__, self.__class__.__name__)
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

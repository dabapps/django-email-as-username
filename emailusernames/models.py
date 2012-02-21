from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from emailusernames.forms import EmailAdminAuthenticationForm
from emailusernames.utils import _email_to_username


# Horrible monkey patching.
# User.username always presents as the email, but saves as a hash of the email.
# It would be possible to avoid such a deep level of monkey-patching,
# but Django's admin displays the "Welcome, username" using user.username,
# and there's really no other way to get around it.
def user_init_patch(self, *args, **kwargs):
    super(User, self).__init__(*args, **kwargs)
    self._username = self.username
    self.username = self.email


def user_save_patch(self, *args, **kwargs):
    self.username = _email_to_username(self.email)
    super(User, self).save(*args, **kwargs)
    self.username = self.email


User.__init__ = user_init_patch
User.save = user_save_patch

# Monkey-path the admin site to use a custom login form
AdminSite.login_form = EmailAdminAuthenticationForm
AdminSite.login_template = 'email_usernames/login.html'

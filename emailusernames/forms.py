from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from emailusernames.utils import user_exists


ERROR_MESSAGE = _("Please enter a correct email and password. ")
ERROR_MESSAGE_RESTRICTED = _("You do not have permission to access the admin.")
ERROR_MESSAGE_INACTIVE = _("This account is inactive.")


class EmailAuthenticationForm(AuthenticationForm):
    """
    Override the default AuthenticationForm to force email-as-username behavior.
    """
    email = forms.EmailField(label=_("Email"), max_length=70)
    message_incorrect_password = ERROR_MESSAGE
    message_inactive = ERROR_MESSAGE_INACTIVE

    def __init__(self, *args, **kwargs):
        super(EmailAdminAuthenticationForm, self).__init__(*args, **kwargs)
        del self.fields['username']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if (self.user_cache is None):
                raise forms.ValidationError(self.message_incorrect_password)
            if not self.user_cache.is_active:
                raise forms.ValidationError(self.message_inactive)
        self.check_for_test_cookie()
        return self.cleaned_data


class EmailAdminAuthenticationForm(AdminAuthenticationForm):
    """
    Override the default AuthenticationForm to force email-as-username behavior.
    """
    email = forms.EmailField(label=_("Email"), max_length=70)
    message_incorrect_password = ERROR_MESSAGE
    message_inactive = ERROR_MESSAGE_INACTIVE
    message_restricted = ERROR_MESSAGE_RESTRICTED

    def __init__(self, *args, **kwargs):
        super(EmailAdminAuthenticationForm, self).__init__(*args, **kwargs)
        del self.fields['username']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if (self.user_cache is None):
                raise forms.ValidationError(self.message_incorrect_password)
            if not self.user_cache.is_active:
                raise forms.ValidationError(self.message_inactive)
            if not self.user_cache.is_staff:
                raise forms.ValidationError(self.message_restricted)
        self.check_for_test_cookie()
        return self.cleaned_data


class EmailUserCreationForm(UserCreationForm):
    """
    Override the default UserCreationForm to force email-as-username behavior.
    """
    email = forms.EmailField(label=_("Email"), max_length=70)

    class Meta:
        model = User
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super(EmailUserCreationForm, self).__init__(*args, **kwargs)
        del self.fields['username']

    def clean_email(self):
        email = self.cleaned_data["email"]
        if user_exists(email):
            raise forms.ValidationError(_("A user with that email already exists."))
        return email


class EmailUserChangeForm(UserChangeForm):
    """
    Override the default UserChangeForm to force email-as-username behavior.
    """
    email = forms.EmailField(label=_("Email"), max_length=70)

    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super(EmailUserChangeForm, self).__init__(*args, **kwargs)
        del self.fields['username']

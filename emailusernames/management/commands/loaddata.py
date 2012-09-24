from django.core.management.commands import loaddata
from emailusernames.models import unmonkeypatch_user


class Command(loaddata.Command):

    """
    Override the built-in loaddata command to un-monkeypatch the User
    model before loading, to allow usernames to be loaded correctly
    """

    def handle(self, *args, **kwargs):
        unmonkeypatch_user()
        return super(Command, self).handle(*args, **kwargs)

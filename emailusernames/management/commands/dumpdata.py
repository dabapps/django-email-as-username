from django.core.management.commands import dumpdata
from emailusernames.models import unmonkeypatch_user


class Command(dumpdata.Command):

    """
    Override the built-in dumpdata command to un-monkeypatch the User
    model before dumping, to allow usernames to be dumped correctly
    """

    def handle(self, *args, **kwargs):
        unmonkeypatch_user()
        return super(Command, self).handle(*args, **kwargs)

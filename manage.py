#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testsettings")

    from django.core.management import execute_from_command_line

    args = sys.argv
    if len(args) == 2 and args[1] == 'test':
        args.append('emailusernames')

    execute_from_command_line(args)

#!/usr/bin/env python
import sys

from django.conf import settings
from django.core.management import execute_from_command_line


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        USE_TZ=True,
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'generic_follow',
            'tests',
        ),
        TEST_RUNNER='django_nose.NoseTestSuiteRunner',
        PASSWORD_HASHERS=('django.contrib.auth.hashers.MD5PasswordHasher',)
    )


def runtests():
    argv = sys.argv[:1] + ['test', 'tests']
    execute_from_command_line(argv)
    sys.exit(0)


if __name__ == '__main__':
    runtests()

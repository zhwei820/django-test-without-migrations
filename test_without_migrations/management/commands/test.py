# coding: utf-8
from optparse import make_option
from django.core.management.commands.test import Command as TestCommand
from django import VERSION as DJANGO_VERSION


class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        if DJANGO_VERSION < (1, 11):
            return "notmigrations"
        if DJANGO_VERSION >= (2, 1):
            return None


class Command(TestCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        # Optparse was deprecated on 1.8
        # So we only define option_list for Django 1.7
        if DJANGO_VERSION < (1, 8):
            self.option_list = super(Command, self).option_list + (
                make_option('-m', '--migrations', action='store_false', dest='nomigrations', default=False,
                help='Tells Django to use migrations before creating tables for tests.'),
            )

    def add_arguments(self, parser):  # New API on Django 1.8
        parser.add_argument(
            '-nm', '--nomigrations', action='store_false', dest='nomigrations',
            default=False,
            help='Tells Django to use migrations before creating tables for tests.'
        )

        super(Command, self).add_arguments(parser)

    def handle(self, *test_labels, **options):
        from django.conf import settings

        if options['nomigrations']:
            settings.MIGRATION_MODULES = DisableMigrations()

        super(Command, self).handle(*test_labels, **options)

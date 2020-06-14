from __future__ import unicode_literals
import os, sys
from django.core.management.base import BaseCommand
from django.contrib.staticfiles import finders
from django.conf import settings

class Command(BaseCommand):
    def clear_dir(self, path):
        self.stdout.write("Clearing dir: " + path)
        for root, dirs, files in os.walk(path):
            if root != path:
                continue

            for name in files:
                self.stdout.write("unlink " + os.path.join(root, name))
                os.unlink(os.path.join(root, name))

            for name in dirs:
                self.stdout.write("unlink " + os.path.join(root, name))
                os.unlink(os.path.join(root, name))

    def make_symbolic_links(self, src_path, dest_path):
        self.stdout.write("Make symbolic links from " + src_path + " to " + dest_path)
        for name in os.listdir(src_path):
            src = os.path.join(src_path, name)
            dest = os.path.join(dest_path, name)
            self.stdout.write(" -> Link dir " + src + " to " + dest)
            os.symlink(src, dest)

    def handle(self, *args, **options):
        print "Links static files"
        paths = finders.find('.', all=True)

        self.clear_dir(settings.STATIC_ROOT)
        for path in paths:
            self.make_symbolic_links(path, settings.STATIC_ROOT)

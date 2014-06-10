from __future__ import unicode_literals

from django.utils.encoding import force_text
from django.conf import settings

from reversion.revisions import default_revision_manager

revision_manager = default_revision_manager
ignore_duplicate_revisions = settings.REVISION_IGNORE_DUPLICATE


class RevisionsMiddleware(object):
    def get_revision_data(self, request):
        """Returns all the revision data to be used in the object's revision."""
        return dict(
            (o, revision_manager.get_adapter(o.__class__).get_version_data(o))
            for o in self.get_revision_instances(request)
        )

    @property
    def revision_context_manager(self):
        """The revision context manager for this VersionAdmin."""
        return revision_manager._revision_context_manager

    def objects_string(self, objects):
        return ', '.join(['%s (%s)' % (force_text(obj._meta.verbose_name), force_text(obj)) for obj in objects])

    def get_log_message(self, request):
        messages = [
                    'Request path: %s' % request.path
                    ]

        if request.added_objects:
            messages.append('New objects: %s' % self.objects_string(request.added_objects))

        if request.changed_objects:
            messages.append('Changed objects: %s' % self.objects_string(request.changed_objects))

        if request.deleted_objects:
            messages.append('Removed objects: %s' % self.objects_string(request.deleted_objects))

        return '\n\n'.join(messages)

    def log(self, request):
        """Sets the version meta information."""
        revision_manager.save_revision(
            self.get_revision_data(request),
            user=request.user,
            comment=self.get_log_message(request),
            ignore_duplicates=ignore_duplicate_revisions,
            db=self.revision_context_manager.get_db(),
        )

    def get_revision_instances(self, request):
        """Returns all the instances to be used in the object's revision."""
        revision_instances = []
        for obj in request.changed_objects + request.added_objects:
            revision_instances.append(obj)
        return revision_instances

    def process_request(self, request):
        request.changed_objects = []
        request.added_objects = []
        request.deleted_objects = []

    def process_response(self, request, response):
        try:
            if request.changed_objects or request.added_objects or request.deleted_objects:
                self.log(request)
        except AttributeError:
            pass
        return response

from __future__ import unicode_literals

from django.conf import settings

from reversion.revisions import default_revision_manager, RegistrationError


class RevisionsMixin(object):

    revision_manager = default_revision_manager
    reversion_format = settings.REVISION_FORMAT

    def __init__(self, *args, **kwargs):
        super(RevisionsMixin, self).__init__(*args, **kwargs)
        self._autoregister(self.model, self.get_follow())

    def get_follow(self):
        return None

    def _autoregister(self, model, follow=None):
        """Registers a model with reversion, if required."""
        if model._meta.proxy:
            raise RegistrationError("Proxy models cannot be used with django-reversion, register the parent class instead")
        if not self.revision_manager.is_registered(model):
            follow = follow or []
            for parent_cls, field in model._meta.parents.items():
                follow.append(field.name)
                self._autoregister(parent_cls)
            self.revision_manager.register(model, follow=follow, format=self.reversion_format)


class RevisionsIsCoreMixin(RevisionsMixin):

    def post_save_model(self, request, obj, form, change):
        if change:
            request.changed_objects.append(obj)
        else:
            request.added_objects.append(obj)

    def pre_delete_model(self, request, obj):
        request.deleted_objects.append(obj)


class RevisionsInlineFormMixin(RevisionsMixin):

    def post_save_obj(self, obj, change):
        if change:
            self.request.changed_objects.append(obj)
        else:
            self.request.added_objects.append(obj)

    def pre_delete_obj(self, obj):
        self.request.deleted_objects.append(obj)


class RevisionsModelFormViewMixin(RevisionsMixin):

    def post_save_obj(self, obj, form, change):
        if change:
            self.request.changed_objects.append(obj)
        else:
            self.request.added_objects.append(obj)

from django.utils.translation import ugettext_lazy as _

from is_core.main import UIRestModelISCore
from is_core.generic_views.inlines.inline_form_views import TabularInlineFormView

from .models import RevisionLog, LogVersion


class LogIsCore(UIRestModelISCore):
    abstract = True

    model = RevisionLog
    list_display = ('date_created', 'user', 'comment')
    rest_list_fields = ('pk',)
    rest_list_obj_fields = ('pk',)
    verbose_name_plural = verbose_name = _('Log')
    menu_group = 'log'

    form_fieldsets = (
        (None, {'fields': ('date_created', 'user', 'comment')}),
        (_('Versions'), {'inline_view': 'VersionInlineFormView'}),
    )
    form_readonly_fields = ('date_created', 'user', 'comment', 'serialized_data')

    def has_create_permission(self, request, obj=None):
        return False

    def has_update_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    class VersionInlineFormView(TabularInlineFormView):
        model = LogVersion
        fields = ('id', 'serialized_data')

    form_inline_views = [VersionInlineFormView]

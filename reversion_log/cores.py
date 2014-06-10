from is_core.main import UIRestModelISCore
from is_core.generic_views.inline_form_views import TabularInlineFormView

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
        (_('Versions'), {'inline_form_view': 'VersionInlineFormView'}),
    )
    form_readonly_fields = ('date_created', 'user', 'comment', 'serialized_data')

    class VersionInlineFormView(TabularInlineFormView):
        model = LogVersion

    inline_form_views = [VersionInlineFormView]

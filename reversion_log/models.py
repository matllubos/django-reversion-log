from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from reversion.models import Version as ReversionVersion, Revision as ReversionRevision


@python_2_unicode_compatible
class RevisionLog(ReversionRevision):

    def __str__(self):
        return '#%s' % self.id

    class Meta:
        proxy = True
        verbose_name = _('Log')
        verbose_name_plural = _('Log')
        ordering = ('-pk',)


class LogVersion(ReversionVersion):

    class Meta:
        proxy = True
        verbose_name = _('Version')
        verbose_name_plural = _('Versions')

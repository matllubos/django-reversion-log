from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from reversion.models import Version as ReversionVersion, Revision as ReversionRevision


class RevisionLog(ReversionRevision):

    def __unicode__(self):
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

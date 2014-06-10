import factory

from reversion import models

from users.tests.models.factories import UserFactory


class RevisionFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = models.Revision

    user = factory.SubFactory(UserFactory)
    comment = factory.Sequence(lambda n: 'Revision coment {0}'.format(n))

import factory

from django.conf import settings


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'Test_User_%s' % n)

    class Meta:
        model = settings.AUTH_USER_MODEL


class RepositoryFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: 'Test_Repository_%s' % n)

    class Meta:
        model = 'mainsite.Repository'


class CommitFactory(factory.django.DjangoModelFactory):
    repository = factory.SubFactory(RepositoryFactory)
    commit_hash = factory.Sequence(lambda n: 'commit_hash_%s' % n)
    branch_name = factory.Sequence(lambda n: 'branch_name_%s' % n)
    # commit_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        model = 'mainsite.Commit'


class TaskFactory(factory.django.DjangoModelFactory):
    opened_in_commit = factory.SubFactory(CommitFactory)

    class Meta:
        model = 'mainsite.Task'

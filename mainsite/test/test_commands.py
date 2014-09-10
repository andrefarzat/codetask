import os

from django.core.management import call_command
from django.test import TestCase
from django.utils import unittest

from codetask.extractor import DirExtractor
from mainsite.management.commands.process_commit import (Command as
                                                         ProcessCommitCommand)
from mainsite.factories import UserFactory, RepositoryFactory


BASE_DIR = os.path.join(os.path.dirname(__file__), 'mockproj')


class TestProcessCommitCommand(TestCase):
    """
    args: 'username repository_name commit_hash branch_name'
    """

    # def test_simple_run(self):
    #     call_command('process_commit', 'p', 'my_repo', 'hashash', 'master')

    def test__get_repository(self):
        user = UserFactory()
        repo = RepositoryFactory(owner=user)
        cmd = ProcessCommitCommand()

        new_repo = cmd._get_repository(user.username, repo.name)
        self.assertEqual(new_repo.id, repo.id)

        new_repo = cmd._get_repository(user.username, 'new_name')
        self.assertNotEqual(new_repo.id, repo.id)
        self.assertEqual(new_repo.name, 'new_name')

    @unittest.skip('will continue')
    def test__process_commit(self):
        user = UserFactory()
        repo = RepositoryFactory(owner=user)
        cmd = ProcessCommitCommand()

        cmd._process_commit(repository=repo, commit_hash='abcd',
                            branch_name='v0')

        self.assertEqual(repo.commits.count(), 1)
        self.assertFail('Continue')


class TestScenario1(TestCase):

    @unittest.skip('Need to use factories')
    def test_sim(self):
        user = User(username='p')
        user.save()
        repository = Repository(owner=user, name='repo_test', type='local')
        repository.save()
        commit = Commit(repository=repository, commit_hash='commit_hash',
                        branch_name='some_branch')
        commit.save()

        dir_extractor = DirExtractor(os.path.join(BASE_DIR, 'v0'))
        for extractor in dir_extractor.get_extractors():
            for extracted_task in extractor.get_tasks():
                task = Task.create_from_extracted_task(extracted_task)
                task.opened_in_commit = commit
                task.save()

        task1 = Task.objects.all()[0]
        self.assertEqual(task1.text, 'task 1')
        self.assertEqual(task1.label, 'todo')

        task2 = Task.objects.all()[1]
        self.assertEqual(task2.username, 'someone')
        self.assertEqual(task2.text, 'make it be something')
        self.assertFalse(task2.closed)

        # phase two
        dir_extractor = DirExtractor(os.path.join(BASE_DIR, 'v0'))

import os

from django.core.management import call_command
from django.test import TestCase

from codetask.extractor import DirExtractor
from mainsite.models import Repository, User, Commit, Task


BASE_DIR = os.path.join(os.path.dirname(__file__), 'mockproj')


class TestProcessCommit(TestCase):
    """
    args: 'username repository_name commit_hash branch_name'
    """

    def test_simple_run(self):
        call_command('process_commit', 'p', 'my_repo', 'hashash', 'master')


class TestScenario1(TestCase):

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

import os

from django.conf import settings
from django.test import TestCase

from codetask.extractor import DirExtractor, ExtractedTask
from mainsite.factories import RepositoryFactory, CommitFactory, TaskFactory
from mainsite.models import Task


class TestRespositoryModel(TestCase):

    def test_get_current_commit(self):
        repo = RepositoryFactory()
        commit = CommitFactory(repository=repo, branch_name='master')
        self.assertEqual(commit, repo.get_current_commit())

        repo = RepositoryFactory()
        with self.assertRaises(repo.DoesNotExist):
            repo.get_current_commit()

    def test_get_path(self):
        repo = RepositoryFactory()
        path = os.path.join(settings.BASE_DIR, 'test', 'mockproj')
        self.assertEqual(repo.get_path(), path)


class TestCommitModel(TestCase):

    def test_get_dir_extractor(self):
        commit = CommitFactory(branch_name='v0')
        self.assertIsInstance(commit.get_dir_extractor(), DirExtractor)


class TestTaskModel(TestCase):

    def test_is_closed_property(self):
        task = TaskFactory(closed_in_commit=CommitFactory())
        self.assertTrue(task.is_closed)

    def test_commit_property(self):
        commit = CommitFactory()
        task = TaskFactory(opened_in_commit=commit)
        self.assertEqual(task.commit, commit)

    def test_filename_property(self):
        task = TaskFactory(filepath='some/path/to/file.txt')
        self.assertEqual(task.filename, 'file.txt')

    def test_create_from_extracted_task(self):
        values = dict(text='text1', filepath='filepath1', line_number=10,
                      label='label1', username='username1')

        extracted_task = ExtractedTask('', '')
        for key, value in values.items():
            setattr(extracted_task, key, value)

        task = Task.create_from_extracted_task(extracted_task)

        for key, value in values.items():
            self.assertEqual(getattr(task, key), value)

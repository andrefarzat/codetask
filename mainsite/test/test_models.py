from django.test import TestCase
from django.utils import unittest

from codetask.extractor import DirExtractor
from mainsite.factories import RepositoryFactory, CommitFactory


class TestRespositoryModel(TestCase):

    def test_get_current_commit(self):
        repo = RepositoryFactory()
        commit = CommitFactory(repository=repo, branch_name='master')
        self.assertEqual(commit, repo.get_current_commit())

        repo = RepositoryFactory()
        with self.assertRaises(repo.DoesNotExist):
            repo.get_current_commit()

    @unittest.skip('Waiting to the method exist')
    def test_get_path(self):
        pass


class TestCommitModel(TestCase):

    @unittest.skip('Waiting to the method exist')
    def test_get_dir_extractor(self):
        commit = Commit()
        self.assertEqual(commit.get_dir_extractor().__class__, DirExtractor)

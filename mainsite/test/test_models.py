from django.test import TestCase
from django.utils import unittest

from codetask.extractor import DirExtractor
from mainsite.models import Commit  # Repository, User, Task


class TestRespositoryModel(TestCase):

    @unittest.skip('Waiting to the method exist')
    def test_get_current_commit(self):
        pass

    @unittest.skip('Waiting to the method exist')
    def test_get_path(self):
        pass


class TestCommitModel(TestCase):

    @unittest.skip('Waiting to the method exist')
    def test_get_dir_extractor(self):
        commit = Commit()
        self.assertEqual(commit.get_dir_extractor().__class__, DirExtractor)

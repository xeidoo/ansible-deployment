# inside test/magic_test.py
# -*- coding: utf-8 -*-
import os
import sys
import unittest
from helper import FakReleases, FakeRelease, FakeAnsibleModule
# Get the right path
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.abspath(dir_path + '/../../library') )
from gh_release import GithubReleases


class TestLatest(unittest.TestCase):
    def test_find_a_release(self):
        fake_ansible = FakeAnsibleModule()
        fake_ansible.params = {"state": "present",
                               "user": "hellofresh",
                               "repo": "ansible-deployment",
                               "dest": "/tmp/dest",
                               "dest_temp": "/tmp/dest",
                               "mode": "get",
                               "version": "latest",
                               "release_type": "release",
                               "token": "xxxx",
                               "download_source": "None",
                               "glob": None}

        gh = GithubReleases(fake_ansible)
        gh.repository = FakReleases("example_release.json")
        result = gh.find_a_release()
        self.assertIsInstance(result, FakeRelease)


class TestPrerelease(unittest.TestCase):
    def test_find_a_release(self):
        fake_ansible = FakeAnsibleModule()
        fake_ansible.params = {"state": "present",
                               "user": "hellofresh",
                               "repo": "ansible-deployment",
                               "dest": "/tmp/dest",
                               "dest_temp": "/tmp/dest",
                               "mode": "get",
                               "version": "latest",
                               "release_type": "prerelease",
                               "token": "xxxx",
                               "download_source": "None",
                               "glob": None}
        gh = GithubReleases(fake_ansible)
        gh.repository = FakReleases("example_release.json")
        self.assertRaises(ValueError, gh.find_a_release)


class TestDraft(unittest.TestCase):
    def test_find_a_release(self):
        fake_ansible = FakeAnsibleModule()
        fake_ansible.params = {"state": "present",
                               "user": "hellofresh",
                               "repo": "ansible-deployment",
                               "dest": "/tmp/dest",
                               "dest_temp": "/tmp/dest",
                               "mode": "get",
                               "version": "latest",
                               "release_type": "draft",
                               "token": "xxxx",
                               "download_source": "None",
                               "glob": None}
        gh = GithubReleases(fake_ansible)
        gh.repository = FakReleases("example_release.json")
        self.assertRaises(ValueError, gh.find_a_release)


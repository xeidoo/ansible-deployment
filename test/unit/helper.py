import json
import argparse as ap

class FakeAnsibleModule:
    check_mode = False
    params = {}

    def fail_json(self, msg=None):
        raise ValueError(msg)


class FakeRelease:
    def __init__(self, file_json):
        with open(file_json) as data_file:
            self.data  = json.load(data_file)
        self.i = 0
        self.n = len(self.data) -1

    def __iter__(self):
        return self

    def next(self):
        if self.i < self.n:
            self.i += 1
            return ap.Namespace(**self.data[self.i])
        else:
            raise StopIteration()


class FakReleases(object):
    def __init__(self, file_json):
        self.file_json = file_json

    def latest_release(self):
        return FakeRelease(self.file_json )

    def releases(self):
        return FakeRelease(self.file_json)

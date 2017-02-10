import json
from ansible.module_utils.urls import open_url


METHOD_GET = 'GET'


class Client(object):
    API_URL = 'https://api.github.com'

    def __init__(self, access_token=None):
        self.access_token = access_token
        self.headers = {}

    def login(self, access_token):
        self.access_token = access_token

    def make_request(self, method, path):
        if self.access_token:
            self.headers = {
                'Authorization': 'token {}'.format(self.access_token)
            }

        result = open_url(
            url=self.API_URL + path,
            method=method,
            headers=self.headers
        )

        return json.load(result)

    def me(self):
        return self.make_request(
            method=METHOD_GET,
            path='/user'
        )

    def repository(self, owner, repo):
        return Repository(
            client=self,
            owner=owner,
            repo=repo
        )


class Repository(object):
    def __init__(self, client, owner, repo):
        self.client = client
        self.owner = owner
        self.repo = repo

    def releases(self):
        releases = self.client.make_request(
            method=METHOD_GET,
            path='/repos/{owner}/{repo}/releases'.format(
                owner=self.owner,
                repo=self.repo
            )
        )

        releases_list = []
        for release in releases:
            releases_list.append(ReleaseModel(release))

        return releases_list

    def latest_release(self):
        return ReleaseModel(self.client.make_request(
            method=METHOD_GET,
            path='/repos/{owner}/{repo}/releases/latest'.format(
                owner=self.owner,
                repo=self.repo
            )
        ))

    def release(self, id):
        return ReleaseModel(self.client.make_request(
            method=METHOD_GET,
            path='/repos/{owner}/{repo}/releases/{id}'.format(
                owner=self.owner,
                repo=self.repo,
                id=id
            )
        ))

    def release_from_tag(self, tag):
        return ReleaseModel(self.client.make_request(
            method=METHOD_GET,
            path='/repos/{owner}/{repo}/releases/tags/{tag}'.format(
                owner=self.owner,
                repo=self.repo,
                tag=tag
            )
        ))


class ReleaseModel(object):
    def __init__(self, data):
        self.data = data

    def __getattr__(self, attr):
        return self.data[attr]

    def assets(self):
        return self.data['assets']

    def archive(self):
        # TODO download archive
        pass

    def json(self):
        return json.dumps(self.data)

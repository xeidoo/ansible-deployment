import urllib2
import json
from ansible.module_utils.urls import open_url


METHOD_GET = 'GET'


class Client(object):
    API_URL = 'https://api.github.com'

    def __init__(self, access_token=None):
        self.access_token = access_token
        self.headers = {}

    def get_authorization_header(self):
        return {
            'Authorization': 'token {}'.format(self.access_token)
        }

    def login(self, access_token):
        self.access_token = access_token

    def request(self, method, path):
        if self.access_token:
            self.headers = self.get_authorization_header()

        result = open_url(
            url=self.API_URL + path,
            method=method,
            headers=self.headers
        )

        return json.load(result)

    def download(self, url, dest, headers={}):
        request = urllib2.Request(url)

        for key, value in headers.iteritems():
            request.add_header(key, value)

        try:
            rsp = urllib2.urlopen(request)
        except Exception as e:
            print e

        f = open(dest, "w")
        while 1:
            data = rsp.read(4096)
            if not data:
                break
            f.write(data)

    def me(self):
        return self.request(
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
        releases = self.client.request(
            method=METHOD_GET,
            path='/repos/{owner}/{repo}/releases'.format(
                owner=self.owner,
                repo=self.repo
            )
        )

        releases_list = []
        for release in releases:
            releases_list.append(ReleaseModel(self.client, release))

        return releases_list

    def latest_release(self):
        return ReleaseModel(
            client=self.client,
            data=self.client.request(
                method=METHOD_GET,
                path='/repos/{owner}/{repo}/releases/latest'.format(
                    owner=self.owner,
                    repo=self.repo
                )
            )
        )

    def release(self, id):
        return ReleaseModel(
            client=self.client,
            data=self.client.request(
                method=METHOD_GET,
                path='/repos/{owner}/{repo}/releases/{id}'.format(
                    owner=self.owner,
                    repo=self.repo,
                    id=id
                )
            )
        )

    def release_from_tag(self, tag):
        return ReleaseModel(
            client=self.client,
            data=self.client.request(
                method=METHOD_GET,
                path='/repos/{owner}/{repo}/releases/tags/{tag}'.format(
                    owner=self.owner,
                    repo=self.repo,
                    tag=tag
                )
            )
        )


class ReleaseModel(object):
    def __init__(self, client, data):
        self.client = client
        self.data = data

    def __getattr__(self, attr):
        return self.data[attr]

    def assets(self):
        assets = []
        for asset in self.data['assets']:
            assets.append(AssetsModel(
                client=self.client,
                data=asset
            ))

        return assets

    def archive(self, source, dest):
        if source not in ['tarball', 'zipball', 'html']:
            raise Exception('%s is not a valid download source')

        self.client.download(
            url=self.data[source + "_url"],
            dest=dest,
            headers=self.client.get_authorization_header()
        )

    def json(self):
        return json.dumps(self.data)


class AssetsModel(object):
    def __init__(self, client, data):
        self.client = client
        self.data = data

    def __getattr__(self, attr):
        return self.data[attr]

    def download(self, dest):
        self.client.download(
            url=self.data['url'],
            dest=dest,
            headers={
                'Accept': 'application/octet-stream'
            }
        )

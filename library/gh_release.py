#!/usr/bin/python

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
import urllib2
import fnmatch
import os
import json

try:
    import semver
    HAS_SEMVER = True
except ImportError:
    HAS_SEMVER = False


METHOD_GET = 'GET'


class GithubClient(object):
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

        rsp = urllib2.urlopen(request)

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
        self.client.download_asset(
            url=self.data['url'],
            dest=dest,
        )


class GithubReleases(object):
    def __init__(self, module):
        self.module = module
        self.token = self.module.params["token"]
        self.dest = self.module.params["dest"]
        self.dest_template = self.module.params["dest_template"]
        self.state = self.module.params["state"]
        self.user = self.module.params["user"]
        self.repo = self.module.params["repo"]
        self.mode = self.module.params["mode"]
        self.version = self.module.params["version"]
        self.release_type = self.module.params["release_type"]
        self.glob = self.module.params["glob"]
        self.download_source = self.module.params["download_source"]
        if self.glob and self.download_source != "None":
            self.module.fail_json(msg="'glob' got '{}' and 'download_source' got '{}' params are mutually exclusive ".format(self.glob, self.download_source))
        ####
        self.full_repo = "{}/{}".format(self.user, self.repo)
        self.github = GithubClient(self.token)
        self.repository = None

    def treat(self):
        return self.version

    def login(self):
        try:
            # test if we're actually logged in
            self.github.me()
        except Exception as e:
            self.module.fail_json(msg="Failed to connect to Github: {}".format(e))

        self.repository = self.github.repository(self.user, self.repo)

    def find_a_release(self):
        if self.version == "latest" and self.release_type == "release":
            return self.repository.latest_release()
        elif self.version == "latest" and self.release_type == "any":
            # We need to filter
            pass
        elif self.version == "latest":
            # We need to filter
            pass
        elif self.version != "latest" and self.release_type == "draft":
            # Specify a draft release version
            for release in self.repository.releases():
                if release.tag_name == self.version:
                    return release
        else:
            # Get a specific release not latest
            release_from_tag = self.repository.release_from_tag(self.version)
            if release_from_tag:
                return release_from_tag
            else:
                # Failed to find tag
                self.module.fail_json(msg="failed to find version {} in repo {}".format(self.version, self.full_repo))

        latest_release = type('obj', (object,), {'tag_name': '0.0.0'})

        for release in self.repository.releases():
            if self.release_type == "any":
                pass
                # don't filter by type
            elif getattr(release, self.release_type):
                try:
                    if semver.compare(release.tag_name, latest_release.tag_name) == 1:
                        latest_release = release
                except ValueError as e:
                    self.module.fail_json(msg="{}".format(e))

        if latest_release.tag_name == '0.0.0':
            self.module.fail_json(msg="failed to find latest release type {} in repo {}"
                                  .format(self.release_type, self.full_repo))

        return latest_release

    def download(self, release):
        # Source download
        if self.download_source is not None and self.download_source != "None":
            return release.archive(self.download_source, self.dest)

        # Look at assets
        assets = release.assets()
        match = 0
        asset_2_download = None
        if self.glob:
            for asset in assets:
                if fnmatch.fnmatch(asset.name, self.glob):
                    asset_2_download = asset
                    match += 1

                if match > 1:
                    self.module.fail_json(msg="Too many files in release '%s' match your glob '%s' please refine it." % (self.version, self.glob))
        else:
            for asset in assets:
                asset_2_download = asset
                match += 1

                if match > 1:
                    self.module.fail_json(msg="Too many files in release '%s' you must specfiy one using the glob options." % self.version)
        if match == 0:
            self.module.fail_json(msg="No assets found for release '%s'" % self.version)

        return asset_2_download.download(self.dest)

    def main(self):
        if self.dest and os.path.exists(self.dest):
            self.module.exit_json(msg="dest '{}' file exists".format(self.dest), dest=self.dest, version=self.version, changed=False)

        self.login()
        release = self.find_a_release()
        if not release:
            self.module.fail_json(msg="Failed to find release")

        # Assign the real github version to local version "so if we use latest it should be resolved
        self.version = release.tag_name

        if self.dest_template:
            self.dest = self.dest.replace("${version}", self.version)

            if os.path.exists(self.dest):
                self.module.exit_json(msg="dest file exists", dest=self.dest, version=self.version, changed=False)

        download = self.download(release)
        if download:
            self.module.exit_json(msg="File downloaded", dest=self.dest, version=self.version, changed=True)

    def usecase(self, opt):
        return opt


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(default="present", choices=["present"]),
            user=dict(required=True, type="str"),
            repo=dict(required=True, type="str"),
            dest=dict(required=False, type="str"),
            dest_template=dict(required=False, type="bool", default=False),
            mode=dict(default="get", choices=["get", "put"]),  # For now we only support getting not releasing
            version=dict(default="latest", type="str"),
            release_type=dict(default="any", choices=["any", "release", "prerelease", "draft"]),
            glob=dict(default=None, type="str"),
            download_source=dict(default="None", choices=["None", "tarball", "zipball"]),
            token=dict(type="str", no_log=True),
        ),
        supports_check_mode=False,
    )

    if not HAS_SEMVER:
        module.fail_json(msg='Missing requried semver module (check docs or install with: pip install semver)')

    GithubReleases(module).main()


if __name__ == '__main__':
    main()

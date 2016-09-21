#!/usr/bin/python

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
import fnmatch
import os
try:
    import github3
    HAS_GITHUB_API = True
except ImportError:
    HAS_GITHUB_API = False

try:
    import semver
    HAS_SEMVER = True
except ImportError:
    HAS_SEMVER = False


class GithubReleases(object):
    def __init__(self, module):
        self.module = module
        self.token = self.module.params["token"]
        self.dest = self.module.params["dest"]
        self.dest_temp = None
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
        if self.dest and self.dest_temp:
            self.module.fail_json(msg="'dest' got '{}' and 'dest_temp' got '{}' params are mutually exclusive ".format(self.dest, self.dest_temp))
        ####
        self.full_repo = "{}/{}".format(self.user, self.repo)
        self.repository = None

    def treat(self):
        return self.version

    def login(self):
        if self.token:
            # login to github
            gh = github3.login(token=str(self.token))
            try:
                # test if we're actually logged in
                gh.me()
            except Exception as e:
                self.module.fail_json(msg="Failed to connect to Github: {}".format(e))

            self.repository = gh.repository(str(self.user), str(self.repo))
        else:
            self.repository = github3.repository(str(self.user), str(self.repo))

    def find_a_release(self):
        if self.version == "latest" and self.release_type == "release":
            return self.repository.latest_release()
        elif self.version == "latest" and self.release_type == "any":
            # We need to filter
            pass
        elif self.version == "latest":
            # We need to filter
            pass
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
            return release.archive("tarball", self.dest)

        # Look at assets
        assets = release.assets()
        match = 0
        asset_2_download = None
        if self.glob:
            for asset in assets:
                if fnmatch.fnmatch(asset.get("name"), self.glob):
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

        if self.dest_temp:
            self.dest_temp = self.dest_temp.replace("${version}", self.version)
            # assign template destination to real
            self.dest = self.dest_temp

            if os.path.exists(self.dest_temp):
                self.module.exit_json(msg="dest_temp file exists", dest=self.dest, version=self.version, changed=False)


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
            dest_temp=dict(required=False, type="str"),
            mode=dict(default="get", choices=["get", "put"]),  # For now we only support getting not releasing
            version=dict(default="latest", type="str"),
            release_type=dict(default="any", choices=["any", "release", "prerelease", "draft"]),
            glob=dict(default=None, type="str"),
            download_source=dict(default="None", choices=["None", "tarball", "zipball"]),
            token=dict(type="str", no_log=True),
        ),
        supports_check_mode=False,
    )
    if not HAS_GITHUB_API:
        module.fail_json(msg='Missing requried github3 module (check docs or install with: pip install github3)')

    if not HAS_SEMVER:
        module.fail_json(msg='Missing requried semver module (check docs or install with: pip install semver)')

    GithubReleases(module).main()

if __name__ == '__main__':
  main()

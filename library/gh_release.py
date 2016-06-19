#!/usr/bin/python
## latest
# https://api.github.com/repos/concourse/autopilot/releases/latest
## 
# https://api.github.com/repos/concourse/autopilot/releases/tags/0.0.2


class GithubReleases(object):
    def __init__(self, module):
        self.module = module
        self.token = self.module.params["token"]
        if self.module.params["token"] is None:
            self.url = "https://api.github.com"
            self.use_token = False
        else:
            self.url = "https://%s@api.github.com" % self.module.params["token"]
            self.use_token = True

        self.state = self.module.params["state"]
        self.repo = self.module.params["repo"]
        self.mode = self.module.params["mode"]
        self.version = self.module.params["version"]
        self.release_type = self.module.params["release_type"]
        self.glob = self.module.params["glob"]
        self.download_source = self.module.params["download_source"]
        
        self.url_2_download = ""
        self.file_2_download = ""

    def get_assets(self):
        # Determine version
        if self.version == "latest":
            constructured_url =  self.url + "/repos/" + self.repo + "/releases/latest"
        else:
            constructured_url =  self.url + "/repos/" + self.repo + "/releases/tags/" + self.version

        try:
            release_response = open_url(constructured_url)
        except urllib2.HTTPError as e:
            self.module.fail_json(msg="Failed to get release infomation. repo='%s' version='%s' tocken='%s' code='%s' error='%s'"  % (self.repo, self.version, self.use_token, e.code, e.reason))
        # Get JSON data
        release_response = json.loads(release_response.read())        
        # Get some info about release
        tag_name = release_response.get("tag_name")
        target_commitish = release_response.get("target_commitish")

        # Source download
        if self.download_source is not None:
            self.url_2_download = release_response.get(self.download_source + "_url" )
        else:
            assets = release_response.get("assets")

            # Fail if we dont have any assets in response
            if len(assets) == 0:
                self.module.fail_json(msg="No downloadable assets in release '%s'. Maybe you wanted to download source tarball/zipball" % tag_name)
            # Check if we match glob
            elif self.glob:
                match = 0
                for asset in assets:
                    if fnmatch.fnmatch(asset.get("name"), self.glob):
                        self.url_2_download = asset.get("browser_download_url")
                        self.file_2_download  = asset.get("name")
                        match += 1
                    if match > 1:
                        self.module.fail_json(msg="To many files in release '%s' match your glob '%s' please refine it." % (tag_name, self.glob))
            # We only have one asset so just use that
            elif len(assets) == 1:
                self.url_2_download = assets[0].get("browser_download_url")
                self.file_2_download  = assets[0].get("name")
            # Wow too many assets fail 
            else:
                file_names = map(lambda x: str(x.get("name")), assets)
                self.module.fail_json(msg="To many files in release '%s' you must specfiy one using the glob options. List of files '%s' " % (tag_name, file_names))

        # lets return of download asset link
        self.module.exit_json(msg="success", tag=tag_name, url=self.url_2_download, commit=target_commitish, changed=False)

    def main(self):
        if self.mode == "get":
            self.get_assets()
        else:
            self.module.fail_json(msg="Mode put is not yet support")
        

def main():
    module = AnsibleModule(
        argument_spec=dict(
            # For now we only support getting not releasing 
            state=dict(default="present", choices=["present"]),
            repo=dict(required=True, type="str"),
            dest=dict(required=True, type="str"),
            mode=dict(default="get", choices=["get","put"]),
            version=dict(default="latest", type="str"),
            release_type=dict(default="any", choices=["any","full-release", "pre-release", "draft"]),
            glob=dict(type="str"),
            download_source=dict(default=None, choices=[None, "tarball", "zipball"]),
            token=dict(type="str", no_log=True),
        ),
        supports_check_mode= True,
        mutually_exclusive = [
                                ['glob', 'download_source'],
                             ],
    )
    GithubReleases(module).main()

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
import json
import fnmatch
      
main()

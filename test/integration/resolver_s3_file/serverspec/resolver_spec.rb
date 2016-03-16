require 'serverspec'

# Required by serverspec
set :backend, :exec

git_hash = "37e85de3e74a94d96ac9c91dbe8a8fb13196b293"

describe file('/opt/manage/test/artifacts') do
    it { should exist }
    it { should be_directory }
    it { should be_mode 755 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
end

describe file("/opt/manage/test/artifacts/test-#{git_hash}.tar.gz") do
    it { should exist }
    it { should be_file }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
end

describe file("/opt/manage/test/src/#{git_hash}") do
    it { should exist }
    it { should be_owned_by 'deploy' }
    it { should be_mode 755 }
    it { should be_grouped_into 'master' }
end

describe file("/opt/manage/test/src/#{git_hash}/#{git_hash}") do
    it { should exist }
    it { should be_owned_by 'deploy' }
    it { should be_mode 755 }
    it { should be_grouped_into 'master' }
end

describe file("/opt/manage/test/current") do
  it { should be_symlink }
  it { should be_linked_to "/opt/manage/test/src/#{git_hash}" }
end

describe file("/opt/manage/test/latest-dev") do
  it { should be_symlink }
  it { should be_linked_to "/opt/manage/test/current" }
end

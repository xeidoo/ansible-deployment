require_relative '../../helper_spec.rb'

git_hash = "f4c25aaf062ab8d1a9079e7b9f9b86a71daa8f2a"

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

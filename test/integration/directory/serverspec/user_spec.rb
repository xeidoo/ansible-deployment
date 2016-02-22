require 'serverspec'

# Required by serverspec
set :backend, :exec

describe group('master') do
  it { should exist }
end

describe user('deploy') do  
  it { should exist }
  it { should belong_to_group 'master' }
  it { should have_home_directory '/opt/manage' }
  it { should have_login_shell '/bin/sh' }
end

describe file("/opt/manage/.ssh/known_hosts") do
    it { should contain 'bitbucket.org' }
    it { should contain 'github.com' }
end


describe file('/opt/manage/theapp') do
    it { should exist }
    it { should be_directory }
    it { should be_mode 0755 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
end
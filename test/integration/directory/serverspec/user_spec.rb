require_relative '../../helper_spec.rb'

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
    it { should_not exist }
end

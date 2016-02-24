require 'serverspec'

# Required by serverspec
set :backend, :exec

describe file('/opt/manage/deployment') do
    it { should exist }
    it { should be_directory }
    it { should be_mode 755 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
end

describe file('/opt/manage/deployment/src') do
    it { should exist }
    it { should be_directory }
    it { should be_mode 755 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
end

describe file('/opt/manage/deployment/src/fdbbc5556e177a831dc0e1fb1dd36bf0e8a9bec2') do
    it { should exist }
    it { should be_directory }
    it { should be_mode 755 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
end

describe file('/opt/manage/deployment/src/fdbbc5556e177a831dc0e1fb1dd36bf0e8a9bec2/.git') do
    it { should_not exist }
end

describe file('/opt/manage/deployment/repo') do
    it { should exist }
    it { should be_directory }
    it { should be_mode 755 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
end

describe file('/opt/manage/deployment/repo/.git') do
    it { should exist }
end

describe file('/opt/manage/deployment/current') do
  it { should be_symlink }
  it { should be_linked_to '/opt/manage/deployment/src/fdbbc5556e177a831dc0e1fb1dd36bf0e8a9bec2' }
end

describe "post deployment check check" do
    describe file('/tmp/deployment_post_check_config_1') do
        it { should exist }
    end

    describe file('/tmp/deployment_post_check_config_2') do
        it { should exist }
    end
end
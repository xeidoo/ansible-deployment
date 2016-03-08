require 'serverspec'

# Required by serverspec
set :backend, :exec


describe file('/opt/manage/theapp') do
    it { should exist }
    it { should be_directory }
    it { should be_mode 755 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
end

# describe file('/opt/manage/theapp/master') do
#     it { should exist }
#     it { should be_directory }
#     it { should be_mode 755 }
#     it { should be_owned_by 'deploy' }
#     it { should be_grouped_into 'master' }
# end

describe file('/var/logs/theapp') do
    it { should exist }
    it { should be_directory }
    it { should be_mode 755 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
end

describe file('/theapp.txt') do
    it { should exist }
    it { should be_file }
    it { should be_mode 644 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
end


require 'serverspec'

# Required by serverspec
set :backend, :exec

describe file('/tmp/parmsfile.txt') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
end

fastcgi_file_content="""#Ansible managed, Don't modify manually

"""

describe file('/tmp/parmsfile.txt') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
end
require 'serverspec'

# Required by serverspec
set :backend, :exec


fastcgi_file_content="""# Ansible managed, Don't modify manually

fastcgi_param myvar1 \"True\";
fastcgi_param myvar2 \"False\";
"""

describe file('/tmp/parmsfile.txt') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
    its(:content) { should match fastcgi_file_content }
end

fastcgi_file_content_1="""# Ansible managed, Don't modify manually

fastcgi_param myvar1 \"False\";
fastcgi_param myvar2 \"False\";
"""

describe file('/tmp/parmsfile_1.txt') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
    its(:content) { should match fastcgi_file_content_1 }
end

fastcgi_file_content_2="""# Ansible managed, Don't modify manually

fastcgi_param myvar1 \"True\";
fastcgi_param myvar2 \"True\";
"""

describe file('/tmp/parmsfile_2.txt') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
    its(:content) { should match fastcgi_file_content_2 }
end

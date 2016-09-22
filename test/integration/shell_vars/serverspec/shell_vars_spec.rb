require_relative '../../helper_spec.rb'

shell_file_contnent="""# Ansible managed, Don't modify manually

export myvar1=\"True\"
export myvar2=\"False\"
"""

describe file('/tmp/shell_vars_file.txt') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
    its(:content) { should match shell_file_contnent }
end

shell_file_contnent_1="""# Ansible managed, Don't modify manually

myvar1=\"False\"
myvar2=\"False\"
"""

describe file('/tmp/shell_vars_file_1.txt') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
    its(:content) { should match shell_file_contnent_1 }
end

shell_file_contnent_2="""# Ansible managed, Don't modify manually

myvar1=\"True\"
myvar2=\"True\"
"""

describe file('/tmp/shell_vars_file_2.txt') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
    its(:content) { should match shell_file_contnent_2 }
end

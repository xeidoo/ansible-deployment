require_relative '../../helper_spec.rb'

shell_file_content_1="""# Ansible managed, Don't modify manually

export myvar1=\"False\"
export myvar2=\"False\"
"""

describe file('/tmp/shell_vars_file_1.txt') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
    its(:content) { should match shell_file_content_1 }
end

shell_file_content_2="""# Ansible managed, Don't modify manually

export myvar1=\"True\"
export myvar2=\"True\"
"""

describe file('/tmp/shell_vars_file_2.txt') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
    its(:content) { should match shell_file_content_2 }
end

shell_file_content_3="""# Ansible managed, Don't modify manually

this is a test myvar1=\"False\"
this is a test myvar2=\"False\"
"""

describe file('/tmp/shell_vars_file_3.txt') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
    its(:content) { should match shell_file_content_3 }
end

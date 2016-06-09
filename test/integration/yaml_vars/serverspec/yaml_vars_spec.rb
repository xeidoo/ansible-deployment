require 'serverspec'

# Required by serverspec
set :backend, :exec


yaml_file_content="""myvar1: 'True'
myvar2: 'False'
"""

describe file('/tmp/yaml_vars_file.yml') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
    its(:content) { should match yaml_file_content }
end

yaml_file_content_1="""myvar1: 'False'
myvar2: 'False'
"""

describe file('/tmp/yaml_vars_file_1.yml') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
    its(:content) { should match yaml_file_content_1 }
end

yaml_file_content_2="""myvar1: 'True'
myvar2: TrueString
"""

describe file('/tmp/yaml_vars_file_2.yml') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
    its(:content) { should match yaml_file_content_2 }
end

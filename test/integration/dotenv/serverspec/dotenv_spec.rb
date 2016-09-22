require_relative '../../helper_spec.rb'

dotenv_file_content="""# Ansible managed, Don't modify manually

myvar1=\"True\"
myvar2=\"False\""""

describe file('/tmp/envfile.txt') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
    its(:content) { should match dotenv_file_content }
end

require_relative '../../helper_spec.rb'

php_pool_file_content_1="""
env[myvar1] = 'False'
env[myvar2] = 'False'
"""

describe file('/tmp/parmsfile_1.txt') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
    its(:content) { should match php_pool_file_content_1 }
end

php_pool_file_content_2="""
env[myvar1] = 'True'
env[myvar2] = 'True'
"""

describe file('/tmp/parmsfile_2.txt') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
    its(:content) { should match php_pool_file_content_2 }
end

require_relative '../../helper_spec.rb'

describe file('/tmp/custom1.txt') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
    its(:content) { should match "1" }
end


describe file('/tmp/custom2.txt') do
    it { should exist }
    it { should be_file }
    it { should be_mode 600 }
    it { should be_owned_by 'deploy' }
    it { should be_grouped_into 'master' }
    its(:content) { should match "2" }
end
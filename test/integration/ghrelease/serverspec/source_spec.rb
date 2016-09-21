require_relative '../../helper_spec.rb'

describe "Source 2.2.0" do
    describe file('/tmp/concourse-2.2.0.tar.gz') do
        it { should exist }
        it { should be_file }
        it { should be_mode 644 }
        it { should be_owned_by 'root' }
        it { should be_grouped_into 'root' }
        its(:sha256sum) { should eq '6e16acf027ce5461a76e342a997afddc5adfd29d9a25af8c16bcf08ae308fbe1' }
    end

    describe file('/tmp/concourse-2.2.0.zip') do
        it { should exist }
        it { should be_file }
        it { should be_mode 644 }
        it { should be_owned_by 'root' }
        it { should be_grouped_into 'root' }
        its(:sha256sum) { should eq '4004f5c2b38e6cc380a8ab5ec171234a1e5a76baecfbf157c739e13d93304909' }
    end
end

describe "Source 2.1.0" do
    describe file('/tmp/concourse-2.1.0.tar.gz') do
        it { should exist }
        it { should be_file }
        it { should be_mode 644 }
        it { should be_owned_by 'root' }
        it { should be_grouped_into 'root' }
        its(:sha256sum) { should eq '3e95c9011fd240078cb5fd77838fe8f83e7e200388013249d5dd9283eb2f4799' }
    end

    describe file('/tmp/concourse-2.1.0.zip') do
        it { should exist }
        it { should be_file }
        it { should be_mode 644 }
        it { should be_owned_by 'root' }
        it { should be_grouped_into 'root' }
        its(:sha256sum) { should eq '709f832de693588ddbb012dff66efad48b1e305bc0ddcc47d096dcc66a5733b3' }
    end
end
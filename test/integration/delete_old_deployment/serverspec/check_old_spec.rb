require_relative '../../helper_spec.rb'

base_dir = "/opt/manage/test"

describe file(base_dir + '/1993e62e54c783cc2b557341fb2d242c7192087a/') do
    it { should_not exist }
end

describe file(base_dir + '/3d057d70ea2047970106edf85f3f070ed75b7956') do
    it { should_not exist }
end

describe file(base_dir + '/2636d85ae49487855de03b7532ef7fca0997423d/') do
    it { should be_directory }
end

describe file(base_dir + '/8cddd0c90615f9910f38dd1bfc938b28b3b0f906/') do
    it { should be_directory }
end

describe file(base_dir + '/a45ca6b47dce563de96582fafad13e47405865b4') do
    it { should be_directory }
end


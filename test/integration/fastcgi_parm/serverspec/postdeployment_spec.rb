require_relative '../../helper_spec.rb'

describe "post deployment check check" do
    describe file('/tmp/deployment_post_check_config_1') do
        it { should exist }
    end

end

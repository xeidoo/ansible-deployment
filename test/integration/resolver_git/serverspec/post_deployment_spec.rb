require 'serverspec'

# Required by serverspec
set :backend, :exec

service_file_contnent="""status
reload
status
stop
start
"""

describe "post deployment check check" do
    describe file('/tmp/deployment_post_check_config_1') do
        it { should exist }
    end

    describe file('/tmp/deployment_post_check_config_2') do
        it { should exist }
    end

    describe file('/tmp/logging_service') do
        it { should exist }
        its(:content) { should match service_file_contnent }
    end
end

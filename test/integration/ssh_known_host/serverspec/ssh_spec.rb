require 'serverspec'

# Required by serverspec
set :backend, :exec

describe file("#{ENV['HOME']}/.ssh/known_hosts") do
    # md5sum of github and bitbucket
    its(:md5sum) { should eq '976a714db5d45f0c8034496bc6e692fa' }
end
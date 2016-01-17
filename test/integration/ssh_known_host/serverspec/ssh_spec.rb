require 'serverspec'

# Required by serverspec
set :backend, :exec

describe file("#{ENV['HOME']}/.ssh/known_hosts") do
    it { should contain 'bitbucket.org' }
    it { should contain 'github.com' }
end

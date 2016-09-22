require_relative '../../helper_spec.rb'

describe "deploy2 user" do

    describe group('master2') do
      it { should exist }
    end

    describe user('deploy2') do
      it { should exist }
      it { should belong_to_group 'master2' }
      it { should have_home_directory '/opt/manage2' }
      it { should have_login_shell '/bin/bash' }
      it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDjEchxV5St8HnM0gemK8QMP5Oy2hRLlHuAdtuETYuCli7WcSCs0kaJOMHkqYfI1cYkpWKPQ4hS66uOf08gH5HVDy2PZ5pRirRjbGJ6UPYpRzL8tns2BrU9LHpioX5lESaQBdD+Cbhu2Wnnk4CNpDrYrlcCDOWPPaN8VYwCX1HZl5aqdaHwWgw6SmDgH9Jd2jOKz6LSHlgtKQ/mA4OOwJxdmNC4pm9+Tu9K5I08mW4vHwiSLG48G9h8d05ZSV5OsK8HnpGKJ4d0fS4qkD57xCMw+9pho/MHurtL0fvDRurm3R6FyoIiHFOPs6dY4rZfYd7ulmHq4dHjN0yzuTtHUvrZ' }
      it { should have_authorized_key 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCwYtOmNysiOHY79umWc+vbxUZu2j/AFqyRvJuMtQDUcUPeWLkCQsRIdgAM1P5yuN3tvktM4Tnuw9yHmKZoKFyKvyDlG5OxA5aOGlKLR91VDr7kHFpzb9UCeAg+Jlzn/xYBLnXvheDEFZPeTyvsd33QSjQhsj1x8JVdUzzpT95nJ+w38HP5J/mAkED4RXPBU1SaOGVyDTkZXg92wTUBAFZDhLelRCrDDAxwc/eHztsT99p+IhC5honWzjndeYd6fdosdXT6CVZDnlQWw8NTdzmCBEuptvYb8Zr+WMBsjJ3nZB7DKnNKb50GXvnLM5/0hv2AltGAy2SPJPRd/6+cCSVV' }
    end

    describe file("/opt/manage2/.ssh/id_rsa") do
      it { should exist }
      it { should be_owned_by 'deploy2' }
      it { should be_grouped_into 'master2' }
      it { should be_mode 600 }
    end

    describe file("/opt/manage2/.ssh/known_hosts") do
        it { should_not exist }
    end



end

# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.env.enable # enable the plugin vagrant-env

  config.vm.hostname = "localhost"
  config.vm.box = 'azure'
  config.vm.network "public_network"
  config.vm.network "private_network",ip: "192.168.56.150", virtualbox__intnet: "vboxnet0"
  config.vm.network "forwarded_port", guest: 80, host: 80

  config.vm.provider :azure do |azure, override|
        # Mandatory Settings
	azure.mgmt_certificate = File.expand_path(ENV['MGMT_CERT'])
	azure.mgmt_endpoint    = "https://management.core.windows.net"
	azure.subscription_id = ENV['SUBSCR_ID']
	azure.vm_name     = ENV['VM_NAME']
	azure.vm_image    = ENV['VM_IMAGE']
	azure.cloud_service_name = ENV['CLOUD_SERVICE_NAME']
	azure.storage_acct_name = ENV['CLOUD_STORAGE_NAME']
	azure.vm_size     = ENV['VM_SIZE']
	config.vm.box_url = ENV['BOX_URL']

	azure.vm_user = ENV['VM_USER'] 
	azure.vm_password = ENV['VM_PASS']

	azure.vm_location = ENV['VM_LOCATION'] # e.g., West US

	azure.ssh_port = "22"
	azure.tcp_endpoints = '8000:80'
  end

  config.ssh.username = ENV['VM_USER'] 
  config.ssh.password = ENV['VM_PASS'] 

  config.vm.synced_folder ".", "/vagrant",disabled: true
  
  #config.ssh.private_key_path = "~/.ssh/id_rsa"
  #config.ssh.forward_agent = true
  
  #config.vm.provision "file", source: "/home/gaby/.ssh/id_rsa.pub", destination: "/home/vagrant/.ssh/me.pub"
  #config.vm.provision "shell", inline: "cat /home/vagrant/.ssh/me.pub >> /home/vagrant/.ssh/authorized_keys"

  # Provision with ansible

  config.vm.provision "ansible" do |ansible|
    ansible.sudo = true
    ansible.playbook = "playbook.yml"
    #ansible.inventory_path = "ansible_hosts"
    # ansible.verbose = "v"
    ansible.host_key_checking = false
    ansible.force_remote_user = ENV['VM_USER']
  end
end

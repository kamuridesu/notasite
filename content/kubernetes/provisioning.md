Title: Provisioning Kubernetes control-plane on a VM using Vagrant
Date: 2022-09-15 17:06

# Tools needed
To deploy our control-plane we need some tools:
- (Vagrant)[https://www.vagrantup.com/]
- (VirtualBox)[https://www.virtualbox.org/]

# Creating Vagrantfile and starting the Virtual Machine
First, create a folder to hold the configs files:
```sh
mkdirs -p $HOME/Documents/KubeDeploy && cd $HOME/Documents/KubeDeploy
```
To initialize our setup, we need to bring a virtual machine with a base image. I'm going to use debian/buster64:
```
vagrant init debian/buster64
```
A new file called `Vagrantfile` is placed on the current directory. This file uses Ruby syntax to tell Vagrant how we want the configuration of our Virtual Machine to be. On my config file, I've added some configs:
```rb
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "debian/buster64"
  config.vm.network "private_network", ip: "192.168.56.10"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = "2"
  end
end
```
To start the VM simply enter the following command:
```
vagrant up
```
And to access the VM enter:
```
vagrant ssh
```

# Deploying Kubernetes
## Setting up required packages
The following packages are needed to install Kubernetes:
- htop
- vim
- apt-transport-https
- ca-certificates
- curl
- software-properties-common
- gnupg
```sh
apt-get update
apt-get upgrade
apt-get install -y htop vim apt-transport-https ca-certificates curl software-properties-common gnupg
```

Then we need to add the repository for Kubernetes and install it:
```sh
touch /etc/apt/sources.list.d/kubernetes.list
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
apt-get update
apt-get install -y kubelet kubeadm kubectl kubernetes-cni
```

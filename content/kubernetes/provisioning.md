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
apt-get upgrade -y
apt-get install -y htop vim apt-transport-https ca-certificates curl software-properties-common gnupg docker docker.io
```
Then we need to add the repository for Kubernetes and install it:
```sh
touch /etc/apt/sources.list.d/kubernetes.list
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
apt-get update -y
apt-get install -y kubelet kubeadm kubectl kubernetes-cni
```
We also need to set `/proc/sys/net/bridge/bridge-nf-call-iptables` to 1 to pass bridged IPV4 traffic to iptables chains, this is a requirement for container network interface plugins. To set, we need to run `sysctl net.bridge.bridge-nf-call-iptables=1`

Now, Kubernetes doesn't supports Docker as a container runtime anymore, so let's use containerd. To get started, download and extract the binaries:
```
curl -L https://github.com/containerd/containerd/releases/download/v1.6.8/containerd-1.6.8-linux-amd64.tar.gz --output /tmp/containerd-1.6.8-linux-amd64.tar.gz
cd /tmp/
tar Cxzvf /usr/local containerd-1.6.8-linux-amd64.tar.gz
```
Containerd doesn't come with a systemd service, to allow systemd to manage containerd, we need to setup the containerd service:
```
mkdir -p /usr/local/lib/systemd/system/
curl -L https://raw.githubusercontent.com/containerd/containerd/main/containerd.service --output /usr/local/lib/systemd/system/containerd.service
systemctl daemon-reload
systemctl enable --now containerd
```
We need to install Runc as a container runtime. Runc is used to run containers process, serving as a low level interface between containers and the Linux system to create and interact with contaieners. It is the reference implementation for the Open Containers Initiative (OCI). The OCI Distribution Spec defines an API protocol to facilitate and standardize the distribution of content.
```
curl -L https://github.com/opencontainers/runc/releases/download/v1.1.4/runc.amd64 --output /tmp/runc.amd64
cd /tmp/
install -m 755 runc.amd64 /usr/local/sbin/runc
```
Now, to get the communication between containers, a plugin for the Container Network Interface (CNI) is needed. Let's install some plugins to allow this:
```
curl -L https://github.com/containernetworking/plugins/releases/download/v1.1.1/cni-plugins-linux-amd64-v1.1.1.tgz --output /tmp/cni-plugins-linux-amd64-v1.1.1.tgz
cd /tmp/
mkdir -p /opt/cni/bin
tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.1.1.tgz
```
One last step before the initial bootstrap of Kubernetes, let's configure the systemd cgroup driver for containerd:
```
mkdir -p /etc/containerd/
containerd config default > /etc/containerd/config.toml
sed -i "s/systemdCgroup = false/systemdCgroup = true/" /etc/containerd/config.toml
```
Aannnd let's bootstrap Kubernetes! I'm using `--apiserver-cert-extra-sans=192.168.56.10` to access the Kubernetes api from outside the Virtual Machine using the custom IP.
````
kubeadm init --pod-network-cidr=192.168.0.0/16 --apiserver-cert-extra-sans=192.168.56.10
export KUBECONFIG=/etc/kubernetes/admin.conf
```
Just as a final touch let's setup Calico, a CNI plugin as well a networking agent provider for pods.
```
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.24.1/manifests/tigera-operator.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.24.1/manifests/custom-resources.yaml
```
And we're done! To see the nodes, type `kubectl get nodes -A`, and to see if all the pods are running, just run `kubectl get pods -A`.

The full scripts is:

```sh
apt-get update
apt-get upgrade -y
apt-get install -y htop vim apt-transport-https ca-certificates curl software-properties-common gnupg docker docker.io

touch /etc/apt/sources.list.d/kubernetes.list
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
apt-get update -y
apt-get install -y kubelet kubeadm kubectl kubernetes-cni

sysctl net.bridge.bridge-nf-call-iptables=1

curl -L https://github.com/containerd/containerd/releases/download/v1.6.8/containerd-1.6.8-linux-amd64.tar.gz --output /tmp/containerd-1.6.8-linux-amd64.tar.gz
cd /tmp/
tar Cxzvf /usr/local containerd-1.6.8-linux-amd64.tar.gz

mkdir -p /usr/local/lib/systemd/system/
curl -L https://raw.githubusercontent.com/containerd/containerd/main/containerd.service --output /usr/local/lib/systemd/system/containerd.service
systemctl daemon-reload
systemctl enable --now containerd

curl -L https://github.com/opencontainers/runc/releases/download/v1.1.4/runc.amd64 --output /tmp/runc.amd64
cd /tmp/
install -m 755 runc.amd64 /usr/local/sbin/runc

curl -L https://github.com/containernetworking/plugins/releases/download/v1.1.1/cni-plugins-linux-amd64-v1.1.1.tgz --output /tmp/cni-plugins-linux-amd64-v1.1.1.tgz
cd /tmp/
mkdir -p /opt/cni/bin
tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.1.1.tgz

mkdir -p /etc/containerd/
containerd config default > /etc/containerd/config.toml
sed -i "s/systemdCgroup = false/systemdCgroup = true/" /etc/containerd/config.toml

kubeadm init --pod-network-cidr=192.168.0.0/16 --apiserver-cert-extra-sans=192.168.56.10
export KUBECONFIG=/etc/kubernetes/admin.conf

kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.24.1/manifests/tigera-operator.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.24.1/manifests/custom-resources.yaml

```
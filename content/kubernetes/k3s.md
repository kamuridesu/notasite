Title: Deploying K3s to Oracle Always Free
Date: 2023-12-26 23:00

# Intro
I've been using an aarch64 VM on Oracle from almost a year now, even this site runs on it. The original infrastructure used Docker Swarm to orchestrate the container, but I experienced some bugs with it, like not creating the service or have conflicts, so I decided to move to Kubernetes.

After searching some ways of running Kubernetes on aarch64, I've found K3s from Rancher. The configuration is pretty much straightforward and it has no complications. This post is part of a serie of posts on how to setup K3s on Oracle using IaC tools, like Terraform, Ansible, Vagrant (for testing), etc.

The way I'm thinking about the infrastructure is the following:

- Setup an AMD64 machine which will handle Load Balacing with HAProxy;
- Setup two aarch64 machines, one with K3s control plane and another worker;
- Use Calico as container network interface;
- Use Istio and Istio Gateway as service mesh;
- Use ArgoCD for deployment of applications;

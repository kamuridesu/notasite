Title: Notes on Kubernetes
Date: 2022-09-09 6:11

# What is Kubernetes?
Kubernetes is a container orchestration tool developed by Google. It helps you to manage containerized applications in different deployments.

What problems does Kubernetes solve?

- Migration from monolith to microservices
- Increased usage of containers
- Proper way to manage containers and environments

What features do orchestration tools offer?

- High Availability
- Scalability
- Disaster recovery (backup and restore)

# Kubernetes Architecture
Control Plane

Nodes (with Kubelet "node agent") running on them. Kubelet is a Kubernetes process that enables clusters to talk to each other and executes tasks.

Each node has containers.

Master nodes (Control plane) runs Kubernetes processes necessary to run and manage the cluster correctly. Some examples:

API Server: it is the entry point process for Kubernetes communication. Other APIs, UIs, and CLI applications use this container to communicate with the cluster.

Controller Manager: Keeps an overview of what is happening on the cluster (create replicas if a pod dies, etc)

Scheduler: Responsible for scheduling containers on different nodes based on workloads and available server resources. It decides where the next containers will be scheduled based on their 

requirements and the resources of the node.

ETCD: a database that holds the current state of the cluster, holding all the configuration and status of each node and container.

Virtual Network turns all the nodes inside of the cluster into one machine.

# Main Kubernetes Components:
## Node and Pod:
Node: A simple physical or virtual server running Kubelet 

Pod: The smallest managed unit in Kubernetes, it's an abstraction over containers, usually running only one application per Pod.

Each Pod gets its own internal IP address

Pods are ephemeral (die very easily), if the container crashes, the Pod will die and a new one will get created with a new IP address.
## Service and Ingress
Service is a static IP address that can be attached to a Pod

The lifecycle of a Pod and a Service are not connected, even if the pod dies, the service stays.

Services can be internal or external, defined on service creation.

Ingress forward to the service
## Config map and Secrets
Configs maps contain configuration data of the applications

Secrets are like config maps but used to store secret data encoded in base64 (the secret components are meant to be encrypted, Kubernetes does not encrypt secrets)

Secrets contain things like passwords, certificates

Reference Secret in pods/deployment
## Volume
If the Pod of an application restarts, the data is gone. But a volume can attach physical storage to the Pod. The storage could be on the local machine, or outside of the cluster. Once a volume is attached to a Pod, the data of the Pod is persistent. Kubernetes does not manage data persistence, so it's up to you or some admin to manage that storage.
## Deployment and StatefulSet
A Deployment is a blueprint for Pods. You create Deployments, where you can specify the number of replicas and the scale conditions. It's an abstraction on top of pods.

Databases cannot be replicated by deployment because they have states, like their data. If you have multiple database containers, you would need something to manage which pods are writing or reading from the storage to avoid inconsistency.  You can use StatefulSets, StatefulSets are made specifically for applications that have states, like databases.

Deployments are useful for Stateless apps and StatefulSets are for stateful apps or databases.

However deploying databases on K8S is more difficult, that's why you'll see databases hosted outside of the cluster more often than inside. Generally, the cluster keeps all the applications that do not have states, using only deployments.
## Wrap up:

- Pod: Abstraction of containers
- Service: Communication
- Ingress: route traffic into the cluster
- Volume: Data persistence
- ConfigMap: External configuration
- Secrets: store secret configuration
- Deployments: stateless replications
- StatefulSet: stateful replications

# Kubernetes Configuration
All the configuration of the Kubernetes cluster goes through a service called API Server (UI, API, CLI, all talks to the API Server). All the communication must be realized through the API Server 
using JSON or YAML.

The configuration is declarative. You say what you expect the result to be and the Controller Manager will do the possible to make sure that the actual state is the desired state.

## Configuration File

The two first lines you use to declare what component you're creating.

Each Configuration File has 3 parts:

1: Metadata: The first part contains the metadata of the component, like the name and labels.

2: Specification: Each component has a specification section where you put what kind of configuration you want to apply to that component.

Inside the specification, the attributes will be specific to the kind of component.

3: Status: Is automatically generated and added by Kubernetes. Kubernetes will always compare the desired state with the actual state and if there is a drift Kubernetes will try to fix that.

Where does Kubernetes get this status data? From ETCD. ETCD holds the current status of any Kubernetes component.

## Format of configuration files

The format of configuration files is YAML. YAML is a human-friendly, easy-to-read data serialization standard. It also is very strict about indentation.

Store the files with your code or in its own git repository.
# What is Minikube and Kubectl
Minikube is a one-node cluster where the master and worker nodes run on the same node.

Kubectl is a command line tool for Kubernetes clusters.

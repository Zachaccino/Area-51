# Area-51

## Deployment from scratch
#### Prerequisites
You'll need:
 1. [ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
 2. [kubectl](https://kubernetes.io/docs/tasks/tools/)
 3. [k3sup](https://github.com/alexellis/k3sup#download-k3sup-tldr)

#### Initial deployment
Before executing these steps, ensure you have an SSH keypair named `Area 51` on openstack and you have the private key at `~/.ssh/area51`. You will also need to fill in your openstack credentials in `openrc.example`.
 1. `mv openrc.example .openrc`
 2. `sudo chmod +x deploy/deploy-k3s-cluster.sh`
 3. `./deploy/deploy-k3s-cluster.sh`

#!/bin/bash
source .openrc
export ANSIBLE_HOST_KEY_CHECKING=False
ansible-playbook ./deployment/deploy-os-hosts.yaml
ansible-playbook -i ./deployment/openstack_inventory.py ./deployment/configure-k3s.yaml

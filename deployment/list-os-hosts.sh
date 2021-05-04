#!/bin/bash
source .openrc
ansible-playbook -i ./deployment/openstack_inventory.py ./deployment/list-os-hosts.yaml

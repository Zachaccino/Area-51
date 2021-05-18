# Area-51

## Deployment from scratch
#### Prerequisites
You'll need:
 1. [ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
 2. [kubectl](https://kubernetes.io/docs/tasks/tools/)
 3. [k3sup](https://github.com/alexellis/k3sup#download-k3sup-tldr)

#### Initial deployment
Before executing these steps, ensure you have an SSH keypair named `Area 51` on openstack and you have the private key at `~/.ssh/area51`. You will also need to `cp openrc.example .openrc`, and then fill in your openstack credentials in `.openrc`. Then:
 1. `sudo chmod +x deploy/deploy-k3s-cluster.sh`
 2. `./deploy/deploy-k3s-cluster.sh`



### Twitter-App 

Few things to note of importance. 

1. The file `twitter_streaming.py` is the main file for executing the app for streaming from the `Dockerfile`. 
2. There are changes still to be made to this file in terms of what data we are to collect from each tweet. We will need to discuss this and agree on what this should look like. 
3. The file `twitter_streaming_into_database.py` is the original version of `twitter_streaming.py` except that it feeds tweets directly into a CouchDB on my local machine. This was mainly for testing as we now need to get the networking setup with the Docker containers for each harvester so as to feed into the database (I don't know how to do this yet).
4. The environment variables (authentication keys) are missing from the `Dockerfile`. We need to add these to each container for each of the harvesters. This can be done in the Dockerfile I'm pretty sure using a `.env` file to accompany the `Dockerfile` but I haven't figured this part out just yet. 
5. I need to put together a `docker-compose.yml` file still. 

To the run the app locally: `docker run --name twitter-streamer -p 5000:5000 -d twitter-streamer`

I still need to review/test some of the above but any help on linking the couchDB setup with the above would be great. I have it working locally but not in a clustered setup. 



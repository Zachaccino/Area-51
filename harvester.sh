export KUBECONFIG=$(pwd)/deployment/kubeconfig
export REMOTE_NODE=$(kubectl get nodes init -o jsonpath={@.status.addresses[0].address})

echo "Building harvester Docker container"
docker build -t $(kubectl get nodes init -o jsonpath={@.status.addresses[0].address}):30002/harvester:latest harvester/
echo "Pushing container to remote Docker registry"
docker push $(kubectl get nodes init -o jsonpath={@.status.addresses[0].address}):30002/harvester:latest
echo "Removing existing deployment"
kubectl delete -f harvester/kube/
echo "Redeploying harvester pod"
kubectl apply -f harvester/kube/
echo "Finshed deploying harvester!"



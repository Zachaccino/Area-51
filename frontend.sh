export KUBECONFIG=$(pwd)/deployment/kubeconfig
export REMOTE_NODE=$(kubectl get nodes init -o jsonpath={@.status.addresses[0].address})

echo "Building frontend Docker container"
docker build -t $(kubectl get nodes init -o jsonpath={@.status.addresses[0].address}):30002/frontend:latest frontend/
echo "Pushing container to remote Docker registry"
docker push $(kubectl get nodes init -o jsonpath={@.status.addresses[0].address}):30002/frontend:latest
echo "Removing existing deployment"
kubectl delete -f frontend/kube/
echo "Redeploying frontend pod"
kubectl apply -f frontend/kube/
echo "Finshed deploying frontend!"



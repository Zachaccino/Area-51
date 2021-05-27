export KUBECONFIG=$(pwd)/deployment/kubeconfig
export REMOTE_NODE=$(kubectl get nodes init -o jsonpath={@.status.addresses[0].address})

echo "Building backend Docker container"
docker build -t $(kubectl get nodes init -o jsonpath={@.status.addresses[0].address}):30002/backend:latest backend/
echo "Pushing container to remote Docker registry"
docker push $(kubectl get nodes init -o jsonpath={@.status.addresses[0].address}):30002/backend:latest
echo "Removing existing deployment"
kubectl delete -f backend/kube/
echo "Redeploying backend pod"
kubectl apply -f backend/kube/
echo "Finshed deploying backend!"



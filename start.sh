#!/bin/bash

minikube start
eval $(minikube docker-env)
docker build -t vk-botfarm-api-botfarm:latest .
docker build -t vk-botfarm-api-database:latest ./database/
kubectl apply -f ./k8s/database-statefulset.yaml
kubectl apply -f ./k8s/database-service.yaml
kubectl apply -f ./k8s/botfarm-deployment.yaml
pod=$(kubectl get pods)
pod=$(echo "$pod" | grep 'botfarm-deployment')
pod=$(echo "$pod" | awk '{print $1}')
forwarding=$(kubectl port-forward $pod 8000:8000)

while [[ $forwarding != *"Forwarding"* ]]
do
    sleep 3
    forwarding=$(kubectl port-forward $pod 8000:8000)
done

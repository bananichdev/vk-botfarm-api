# Ботоферма VK
## Документация
Все эндпоинты и документацию OpenAPI можно посмотреть (Предварительно, запустив сервис), перейдя по ссылке [http://localhost:8000/api/v1/botfarm/docs](http://localhost:8000/api/v1/botfarm/docs)
## Как запустить?
### Doker-compose
<b>Должен быть установлен docker</b><br>
Если хотите видеть логи контейнеров:
```shell
docker compose up
```
Если не хотите видеть логи контейнеров:
```shell
docker compose up -d
```
Остановить сервис:
```shell
docker compose stop
```

### Minikube
<b>Должен быть установлен kubectl и minikube</b><br>

```shell
minikube start
```
```shell
eval $(minikube docker-env)
docker build -t vk-botfarm-api-botfarm:latest .
docker build -t vk-botfarm-api-database:latest ./database/
```
```shell
kubectl apply -f ./k8s/database-statefulset.yaml
```
```shell
kubectl apply -f ./k8s/database-service.yaml
```
```shell
kubectl apply -f ./k8s/botfarm-deployment.yaml
```
```shell
kubectl port-forward <pod-name> 8000:8000
```
Чтобы получить <pod-name>, напишите:
```shell
kubectl get pods
```
и скопируйте название пода, начинающегося с botfarm-deployment

Остановить сервис:
```shell
minikube stop
```

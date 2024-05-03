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
bash start.sh
```

Остановить сервис:
```shell
bash stop.sh
```

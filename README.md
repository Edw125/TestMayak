# TestMayak
# Как развернуть проект в Docker:
* Запустите терминал. Убедитесь, что вы находитесь в той же
директории, где сохранён Dockerfile

* Откройте Dockerfile любым редактором и впишите ваш `TELEGRAM_TOKEN` в соответствующую переменную.
Пример: `TELEGRAM_TOKEN="5041194628:HNBFR3Aefv8VEdREBCRL3WV49dhFu8fYr54"`
* Запустите сборку образа:
```
docker build -t <image name> .
```
Просмотреть образы в терминале:
```
docker image ls 
```
Запуск контейнера (если запуск из windows, дописать в начало строки 'winpty'):
```
docker run --name <container name> -it  -p 8000:80 <image name>
```
Просмотр всех контейнеров:
``` 
docker container ls -a
```
Запустить контейнер:
```
docker container stop <CONTAINER ID> 
```
Остановить контейнер:
```
docker container start <CONTAINER ID> 
```
Список всех команд для работы с контейнером можно вызвать через:
```
docker container 
```
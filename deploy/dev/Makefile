PROCESS_MANAGER_API_MYSQL_HOST_PORT=3329
PROCESS_MANAGER_API_WEB_HOST_PORT=8029
PROCESS_MANAGER_ADMIN_MYSQL_HOST_PORT=3330
PROCESS_MANAGER_ADMIN_WEB_HOST_PORT=8030
GENOPEDIA_PROCESS_MANAGER_HOME=$(GENOPEDIA_HOME)/genopedia-process-manager

create-storage:
	sudo docker run -d --name=genopedia-dev.process-manager-api.mysql.storage \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1 true
	sudo docker run -d --name=genopedia-dev.process-manager-admin.mysql.storage \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1 true

clear-storage:
	-sudo docker stop genopedia-dev.process-manager-api.mysql.storage
	-sudo docker rm genopedia-dev.process-manager-api.mysql.storage
	-sudo docker stop genopedia-dev.process-manager-admin.mysql.storage
	-sudo docker rm genopedia-dev.process-manager-admin.mysql.storage

deploy:
	sudo docker run -d --name=genopedia-dev.process-manager-api.mysql \
		--volumes-from=genopedia-dev.process-manager-api.mysql.storage \
		-p $(PROCESS_MANAGER_API_MYSQL_HOST_PORT):3306 \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1
	sudo docker run -d --name=genopedia-dev.process-manager-api.web \
		--link genopedia-dev.process-manager-api.mysql:mysql \
		-v $(GENOPEDIA_PROCESS_MANAGER_HOME)/api-web/src/www:/opt/www \
		-p $(PROCESS_MANAGER_API_WEB_HOST_PORT):80 \
		genopedia/process-manager/api-web/dev

	sudo docker run -d --name=genopedia-dev.process-manager-admin.mysql \
		-p $(PROCESS_MANAGER_ADMIN_MYSQL_HOST_PORT):3306 \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1
	sudo docker run -d --name=genopedia-dev.process-manager-admin.web \
		--link genopedia-dev.process-manager-admin.mysql:mysql \
		--link genopedia-dev.process-manager-api.web:process-manager-api \
		-v $(GENOPEDIA_PROCESS_MANAGER_HOME)/admin-web/src/www:/opt/www \
		-p $(PROCESS_MANAGER_ADMIN_WEB_HOST_PORT):80 \
		genopedia/process-manager/admin-web/dev

	sudo cp nginx/genopedia-process-manager-api-web /etc/nginx/sites-enabled
	sudo cp nginx/genopedia-process-manager-admin-web /etc/nginx/sites-enabled
	sudo service nginx reload

	sleep 10

	-sudo docker exec -it genopedia-dev.process-manager-api.mysql mysql -uroot -p123456 -e "CREATE DATABASE IF NOT EXISTS api_db;"
	-sudo docker exec -it genopedia-dev.process-manager-api.web python /opt/www/manage.py migrate

	-sudo docker exec -it genopedia-dev.process-manager-admin.mysql mysql -uroot -p123456 -e "CREATE DATABASE IF NOT EXISTS admin_db;"
	-sudo docker exec -it genopedia-dev.process-manager-admin.web python /opt/www/manage.py migrate
	-sudo docker exec -it genopedia-dev.process-manager-admin.web python /opt/www/manage.py linkstatic

clean:
	-sudo docker stop genopedia-dev.process-manager-admin.mysql
	-sudo docker stop genopedia-dev.process-manager-admin.web
	-sudo docker stop genopedia-dev.process-manager-api.mysql
	-sudo docker stop genopedia-dev.process-manager-api.web

	-sudo docker rm genopedia-dev.process-manager-admin.mysql
	-sudo docker rm genopedia-dev.process-manager-admin.web
	-sudo docker rm genopedia-dev.process-manager-api.mysql
	-sudo docker rm genopedia-dev.process-manager-api.web

	-sudo rm /etc/nginx/sites-enabled/genopedia-process-manager-api-web
	-sudo rm /etc/nginx/sites-enabled/genopedia-process-manager-admin-web

start:
	sudo docker start genopedia-dev.process-manager-api.mysql
	sudo docker start genopedia-dev.process-manager-api.web
	sudo docker start genopedia-dev.process-manager-admin.mysql
	sudo docker start genopedia-dev.process-manager-admin.web

stop:
	sudo docker stop genopedia-dev.process-manager-api.mysql
	sudo docker stop genopedia-dev.process-manager-api.web
	sudo docker stop genopedia-dev.process-manager-admin.mysql
	sudo docker stop genopedia-dev.process-manager-admin.web

migrate:
	-sudo docker exec -it genopedia-dev.process-manager-api.web python /opt/www/manage.py migrate
	-sudo docker exec -it genopedia-dev.process-manager-admin.web python /opt/www/manage.py migrate

ssh-api-mysql:
	sudo docker exec -it genopedia-dev.process-manager-api.mysql bash

ssh-api-web:
	sudo docker exec -it genopedia-dev.process-manager-api.web bash

ssh-admin-mysql:
	sudo docker exec -it genopedia-dev.process-manager-admin.mysql bash

ssh-admin-web:
	sudo docker exec -it genopedia-dev.process-manager-admin.web bash

exec-start-services:
	sudo docker exec -it genopedia-dev.process-manager-api.web python /opt/www/manage.py start_services

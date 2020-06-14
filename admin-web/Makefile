REGISTRY=registry.novogenialab.com

build:
	sudo docker build -f docker/Dockerfile-dev -t genopedia/process-manager/admin-web/dev .

release-test:
	sudo docker build --no-cache -f docker/Dockerfile-test -t genopedia/process-manager/admin-web/test .
	sudo docker tag genopedia/process-manager/admin-web/test $(REGISTRY)/genopedia/process-manager/admin-web/test
	sudo docker push $(REGISTRY)/genopedia/process-manager/admin-web/test

release-prod:
	sudo docker build --no-cache -f docker/Dockerfile-prod -t genopedia/process-manager/admin-web/prod .
	sudo docker tag genopedia/process-manager/admin-web/prod $(REGISTRY)/genopedia/process-manager/admin-web/prod
	sudo docker push $(REGISTRY)/genopedia/process-manager/admin-web/prod

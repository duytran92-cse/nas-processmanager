REGISTRY=registry.novogenialab.com

build:
	sudo docker build -f docker/Dockerfile-dev -t genopedia/process-manager/api-web/dev .

release-test:
	sudo docker build --no-cache -f docker/Dockerfile-test -t genopedia/process-manager/api-web/test .
	sudo docker tag genopedia/process-manager/api-web/test $(REGISTRY)/genopedia/process-manager/api-web/test
	sudo docker push $(REGISTRY)/genopedia/process-manager/api-web/test

release-prod:
	sudo docker build --no-cache -f docker/Dockerfile-prod -t genopedia/process-manager/api-web/test .
	sudo docker tag genopedia/process-manager/api-web/prod $(REGISTRY)/genopedia/process-manager/api-web/prod
	sudo docker push $(REGISTRY)/genopedia/process-manager/api-web/prod

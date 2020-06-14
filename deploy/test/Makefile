
deploy:
	kubectl apply -f mysql.yaml
	kubectl apply -f api-web.yaml
	kubectl apply -f api-start-services.yaml
	kubectl apply -f admin-web.yaml

clean-and-db:
	kubectl delete -f api-web.yaml
	kubectl delete -f admin-web.yaml
	kubectl delete -f mysql.yaml

clean-no-db:
	kubectl delete -f api-web.yaml
	kubectl delete -f admin-web.yaml

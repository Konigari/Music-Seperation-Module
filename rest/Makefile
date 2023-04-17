VERSION=v1
ALIAS=latest
DOCKERUSER=nrvinay08

build:
	docker build -t demucs-rest .

# docker tag demucs-rest nrvinay08/demucs-rest:latest
# docker tag demucs-rest nrvinay08/demucs-rest:v1
# docker push nrvinay08/demucs-rest:latest
# docker push nrvinay08/demucs-rest:v1
push:
	docker tag demucs-rest $(DOCKERUSER)/demucs-rest:$(VERSION)
	docker push $(DOCKERUSER)/demucs-rest:$(VERSION)
	docker tag demucs-rest $(DOCKERUSER)/demucs-rest:${ALIAS}
	docker push $(DOCKERUSER)/demucs-rest:${ALIAS}

deploy:
	kubectl config use-context lab7
	kubectl apply -f rest-deployment.yaml
	kubectl apply -f rest-service.yaml
	kubectl apply -f rest-ingress.yaml

clean:
	kubectl config use-context lab7
	kubectl delete deployment/backend-dep
	kubectl delete service/backend-svc
	kubectl delete ingress/backend-ing
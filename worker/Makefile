VERSION=v1
DOCKERUSER=rachna27

build:
	docker build -f Dockerfile -t demucs-worker .

# docker tag dw nrvinay08/demucs-worker:latest
# docker tag demucs-worker nrvinay08/demucs-worker:v1
# docker push nrvinay08/demucs-worker:latest
# docker push nrvinay08/demucs-worker:v1

push:
	docker tag demucs-worker $(DOCKERUSER)/demucs-worker:$(VERSION)
	docker push $(DOCKERUSER)/demucs-worker:$(VERSION)
	docker tag demucs-worker $(DOCKERUSER)/demucs-worker:latest
	docker push $(DOCKERUSER)/demucs-worker:latest

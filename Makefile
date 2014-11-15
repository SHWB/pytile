.PHONY: all test containerized-test

all: test

test:
	python test/detect_clusters_test.py 
	python test/segment_test.py

docker/.built: docker/Dockerfile
	docker build -t pytile-testenv docker/
	touch docker/.built

containerized-test: docker/.built
	docker run -ti --rm -v $$(readlink -f .):/pytile pytile-testenv /bin/bash -c "cd /pytile && make test"
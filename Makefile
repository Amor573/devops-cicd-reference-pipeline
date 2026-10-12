.PHONY: test run helm-lint docker-build
test:
	python -m unittest discover -s tests -v
run:
	python -m src.app
helm-lint:
	helm lint charts/platform-demo
	helm template platform-demo charts/platform-demo
docker-build:
	docker build -t platform-demo:local .

RUN_IN_DOCKER = docker-compose run --rm --user $$(id -u)\:$$(id -g)


image.build: Dockerfile docker-compose.yaml
	docker-compose build

sh: image.build
	${RUN_IN_DOCKER} --entrypoint sh advent-of-code

tests: image.build
	${RUN_IN_DOCKER} advent-of-code pytest --durations=0 --benchmark-disable

benchmark: image.build
	${RUN_IN_DOCKER} advent-of-code pytest --durations=0



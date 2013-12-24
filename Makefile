all:
	$(info Sorry, not going to run `all`. Try a specific command.)

.PHONY: mongo-server redis-server orl-server

mongo-server: Dockerfile.mongo
	docker build -t openrunlog/mongo-server - < Dockerfile.mongo

redis-server: Dockerfile.redis
	docker build -t openrunlog/redis-server - < Dockerfile.redis

orl-server: Dockerfile
	docker build -t openrunlog/orl-server .

docker-all: mongo-server redis-server orl-server

create-all:
	docker run -d -p 27017:27017 -name mongo openrunlog/mongo-server
	docker run -d -p 6379:6379 -name redis openrunlog/redis-server
	docker run -d -p 11000:11000 \
		-link redis:redis \
		-link mongo:mongo \
		-v `pwd`:/openrunlog \
		openrunlog/orl-server

start-all:
	docker start `docker ps -a | grep -m 1 mongo-server | cut -d' ' -f1`
	docker start `docker ps -a | grep -m 1 redis-server | cut -d' ' -f1`
	docker start `docker ps -a | grep -m 1 orl-server | cut -d' ' -f1`

stop-all:
	docker stop `docker ps | grep -m 1 orl-server | cut -d' ' -f1`
	docker stop `docker ps | grep -m 1 redis-server | cut -d' ' -f1`
	docker stop `docker ps | grep -m 1 mongo-server | cut -d' ' -f1`

# ex: set noexpandtab tabstop=4

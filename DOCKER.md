# Setting up Docker-world!

Checkout the `docker` branch of `github.com/bkendall/openrunlog`

## Installing Docker on a Mac [IMPORTANT]

Basically, follow the instructions found [here](http://docs.docker.io/en/latest/installation/vagrant/), but before you run `vagrant up`, edit the `Vagrantfile`. Add the line `config.vm.forward_port 11000, 11000` after the line `config.ssh.forward_agent = true`. This enables port forwarding from the vagrant image to your local Mac.

This means these instructions boil down to:

    git clone https://github.com/dotcloud/docker.git
    cd docker
    vim Vagrantfile # [[edit file as described above]]
    vagrant up

    vagrant ssh

You then have an environment set up with `docker` and you can continue with the instructions.

## Setting Up Images [Makefile]

The following set of commands will get you up and running with Docker using your local repository as the source for the server running. This means any changes you make locally are seen by the `orl-server` image and the server updates appropriately.

    sudo make docker-all
    sudo make create-all

Once you've created the image once, you will not need to re-create them. You can then use the following to start/stop the server containers:

    sudo make start-all
    sudo make stop-all

## Setting Up Images [Manually]

At this point, you should have `docker` available to you. Congrats.

Be in the root of the `docker` branch of the repo.

Build the 3 images (for mongo, redis, and openrunlog):

    docker build -t openrunlog/mongo-server - < Dockerfile.mongo
    docker build -t openrunlog/redis-server - < Dockerfile.redis
    docker build -t openrunlog/orl-server .

Then, start them up, must start openrunlog last:

    docker run -d -p 27017:27017 -name mongo openrunlog/mongo-server
    docker run -d -p 6379:6379 -name redis openrunlog/redis-server
    docker run -d -p 11000:11000 -link redis:redis -link mongo:mongo openrunlog/orl-server

## Verify Images Running

The quickest way to verify that the containers are now running is to run `curl localhost:11000` on the docker host (from the vagrant image that you're 'ssh-d' into) and see that you actually get HTML back.

## Verify Access From Mac (if on Mac)

After you verify that the containers are running from the docker image (vagrant machine) point of view, you should be able to access ORL from [`http://localhost:11000`](http://localhost:11000) on your Mac (grandparent host?) machine.

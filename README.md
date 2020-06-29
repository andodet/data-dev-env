# Test development environment

Spin up a development environment wiht a populated db through `docker-compose` and
[`Faker`](https://faker.readthedocs.io/en/master/).

# Db Schema

As a pure example, the image will spin up a MySQL db populated with:

- `users`: table containing information on users.
- `transactions`: table containing transactions.

`Faker` offers a number of data [providers](https://faker.readthedocs.io/en/master/providers.html)
that make fairly trivial to replicate pretty much any production set-up.

# Installation

Build the image and spin the containers by launching:

```sh
docker-compose up --build
```

You can then explore the fresh MySQL database with any given client:
```sh
mysql -h 0.0.0.0 -P 3306 -u root -p root
```

# Extras

`docker-compose.cli.yaml` spins up an extra container to run tests to check 
that all the necessary tables have been correctly created. This can be easily integrated 
into a CI pipeline similarly to the setup achieved in this repo through Github Actions.
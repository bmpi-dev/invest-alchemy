# Invest Alchemy Core Service

## Infrastructure

[serverless-jobs-using-fargate](https://github.com/z0ph/serverless-jobs-using-fargate)

- First need install terraform(v1.2.6)
  - https://learn.hashicorp.com/tutorials/terraform/install-cli
- Then `make init`

## How to start

### env

```
mv .env_sample .env # must set .env
source .env
```

### Docker

```
docker build -t invest-alchemy-core .
docker run -t -i -e TUSHARE_API_TOKEN=xxxx -e TG_BOT_API_TOKEN=xxxx -e TG_CHAT_IDS='123,xxx 456,yyy' -e PG_DB_URL=xxxx -e PG_DB_PWD=xxxx invest-alchemy-core
```

#### push docker to AWS ECR

```
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 745121664662.dkr.ecr.us-east-1.amazonaws.com # Retrieve an authentication token and authenticate your Docker client to your registry

docker build -t invest-alchemy-core . # Build your Docker image

docker tag invest-alchemy-core:latest 745121664662.dkr.ecr.us-east-1.amazonaws.com/invest-alchemy-core:latest # tag your image so you can push the image to this repository

docker push 745121664662.dkr.ecr.us-east-1.amazonaws.com/invest-alchemy-core:latest # push this image to your newly created AWS repository
```

## Workflow

change src code -> make build-docker -> make apply

## Note

### Database

#### Liquibase Database Migration

**Warning**: Database migration is required every time the database schema changes!

> Considering that the number of database schema changes is very small, there is no need to do automatic migration because it will introduce complexity.

First it must configure Liquibase's configuration file, copy `src/db/liquibase.properties.tmp` to `src/db/liquibase.properties`, then modify it with the real postgres configuration.

After it, just execute this command in `src` directory.

```bash
python3 other/main_db_migrate.py
```

#### Peewee Model

```bash
python3 -m pwiz -e sqlite /tmp/invest-alchemy/base.db # generate peewee model from sqlite database
```

### S3

S3 bucket enable versioning to prevent accidental database deletion, the version lifecycle rule is:
  - Day 0
    - Objects become noncurrent
  - Day 7
    - 3 newest noncurrent versions are retained
    - All other noncurrent versions are permanently deleted
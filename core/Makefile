.DEFAULT_GOAL := help

help:
	@echo "${PROJECT}"
	@echo "${DESCRIPTION}"
	@echo ""
	@echo "	artifacts - create the S3 artifacts bucket used for Remote TFSTATE"
	@echo "	build-docker - Build and push docker image"
	@echo "	init - init terraform backend"
	@echo "	validate - validate IaC"
	@echo "	plan - init, validate and plan (dry-run) IaC using Terraform"
	@echo "	apply - deploy the IaC using Terraform"
	@echo "	destroy - delete all previously created infrastructure using Terraform"
	@echo "	clean - clean the build folder"


################ Project #######################
PROJECT ?= invest-alchemy-core
DESCRIPTION ?= invest alchemy core service

################################################

################ Config ########################
S3_BUCKET ?= invest-alchemy
AWS_REGION ?= us-east-1
ENV ?= dev
ECR := 745121664662.dkr.ecr.us-east-1.amazonaws.com/invest-alchemy-core-ecr-dev # ECR Repository Example: 123456789012.dkr.ecr.eu-west-1.amazonaws.com/{project_name}-ecr-{env}
################################################

################ Artifacts Bucket ##############
artifacts:
	@echo "Creation of artifacts bucket"
	@aws s3 mb s3://$(S3_BUCKET)
	@aws s3api put-bucket-encryption --bucket $(S3_BUCKET) \
		--server-side-encryption-configuration \
		'{"Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]}'
	@aws s3api put-bucket-versioning --bucket $(S3_BUCKET) --versioning-configuration Status=Enabled
################################################


build-docker:
	@echo "run aws ecr get-login --region $(AWS_REGION) first"
	@docker build -t $(PROJECT) .
	@docker tag $(PROJECT) $(ECR)
	@docker push $(ECR)

################ Terraform #####################

init:
	@. .env
	@./terraform -chdir=./Infrastructure/tf-fargate/ init \
		-backend-config="bucket=$(S3_BUCKET)" \
		-backend-config="key=$(PROJECT)/terraform.tfstate" \

validate:
	@terraform -chdir=./Infrastructure/tf-fargate/ validate

plan:
	@terraform -chdir=./Infrastructure/tf-fargate/ plan \
		-var="env=$(ENV)" \
		-var="project=$(PROJECT)" \
		-var="description=$(DESCRIPTION)" \
		-var="aws_region=$(AWS_REGION)" \
		-var="artifacts_bucket=$(S3_BUCKET)" \

apply:
	@terraform -chdir=./Infrastructure/tf-fargate/ apply \
		-var="env=$(ENV)" \
		-var="project=$(PROJECT)" \
		-var="description=$(DESCRIPTION)" \
		-compact-warnings

destroy:
	@read -p "Are you sure that you want to destroy: '$(PROJECT)-$(ENV)-$(AWS_REGION)'? [yes/N]: " sure && [ $${sure:-N} = 'yes' ]
	@terraform -chdir=./Infrastructure/tf-fargate/ destroy

clean:
	@rm -fr build/
	@rm -fr dist/
	@rm -fr htmlcov/
	@rm -fr site/
	@rm -fr .eggs/
	@rm -fr .tox/
	@rm -fr *.tfstate
	@rm -fr *.tfplan
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '.DS_Store' -exec rm -fr {} +
	@find . -name '*.egg' -exec rm -f {} +
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +
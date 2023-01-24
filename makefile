###
# Makefile
# Instalção do ambiente de Desenvolvimento,
# ferramentas de qualidade de código e testes.
###
format:  ## Formata o código.
	@echo ""
	@echo "============ Formatando do código ============"
	@echo "Ordenando os Imports"
	@poetry run isort .
	@echo "Formatação do código com Blue(Black)"
	@poetry run blue .

lint:format ## Roda o format, antes roda o lint.
	@echo "============ Padronizando o código ============"
	@echo "Executando o Flake8"
	@poetry run flake8 .
	@echo "Executando o Isort"
	@poetry run isort --diff -c .
	@echo "Executando o Blue"
	@poetry run blue --check --diff --color .

audit: ## Auditoria
	@echo "============ Auditando o código e as dependências ============"
	@echo "Executando o PyUpgrade"
	@poetry run pyupgrade --py310-plus **/*.py
	@echo "Executando o Bandit"
	@poetry run bandit -r app/
	@echo "Executando o Pip-Audit: Verificar o log em logs/pip-audit.log"
	@poetry run pip-audit --ignore GHSA-w596-4wvx-j9j6 -f json -d --fix -v -o ./logs/pip-audit.json &> /dev/null

test: ## Roda os testes.
	@echo "============ Executando os testes ============"
	@poetry run pytest -vv -s --cov-report=term-missing --cov-report html --cov-branch --cov=tests/

#################################### Development Env ################################
# Instalação do ambiente de desenvolvimento
env:
	@echo "Criando o ambieente virtual."
	python3 -m venv .venv

dependencies: hooks ## Instala as dependências do projeto.
	@echo "Instalando o Poetry."
	pip install --upgrade Pip
	pip install poetry
	poetry config virtualenvs.in-project true
	poetry install

dev_run:
	@echo "============ Executando o projeto ============"
	poetry run flask --app run --debug run

dev_run_gunicorn:
	@echo "============ Executando o projeto ============"
	poetry run gunicorn --bind ":5000" run:app -w 4 -t 30
#################################### ./Development Env ##################################
######################################## GIT HOOKS ######################################
hooks:
	@echo "Configurando o Git Hooks."
# Verifica o VCS e adiciona os hooks
	@ if [ -d .git ]; then \
		echo "$$git_pre_commit" > .git/hooks/pre-commit; \
		echo "$$git_pre_push" > .git/hooks/pre-push; \
		chmod +x .git/hooks/pre-*; \
	fi

	@ if [ -d .hg ]; then \
		echo "$$hg_hooks" > .hg/hgrc; \
	fi

# Pre-commit
define git_pre_commit
#!/bin/bash
cd $$(git rev-parse --show-toplevel)
poetry run make lint
endef
export git_pre_commit

## Pre-push
define git_pre_push
#!/bin/bash
cd $$(git rev-parse --show-toplevel)
poetry run make test
endef
export git_pre_push

# Git Hooks
define hg_hooks
[hooks]
precommit.lint = (cd `hg root`; poetry run make lint)
pre-push.test = (cd `hg root`; poetry run make test)
endef
export hg_hooks
######################################## ./GIT HOOKS #####################################
######################################## DOCKER ##########################################
docker_build:
	@echo "Build - Criando a imagem docker."
	docker build -t alm:latest . --no-cache

docker_run:
	@echo "Iniciando container."
	docker run -it -d -p 5000:5000 alm
######################################## ./DOCKER ########################################
create_module: ## Cria um novo módulo.
	@echo "============ Criando um novo módulo ============"
	@echo "Digite o nome do módulo: "
	@read module_name; \
	echo "Criando o módulo: $$module_name"; \
	mkdir -p app/$$module_name; \
	touch app/$$module_name/__init__.py; \
	mkdir -p app/$$module_name/controllers; \
	touch app/$$module_name/controllers/__init__.py; \
	touch app/$$module_name/controllers/$$module_name"_controller.py"; \
	mkdir -p app/$$module_name/models; \
	touch app/$$module_name/models/__init__.py; \
	mkdir -p app/$$module_name/repositories; \
	touch app/$$module_name/repositories/__init__.py; \
	touch app/$$module_name/repositories/$$module_name"_repository.py"; \
	mkdir -p app/$$module_name/routes; \
	touch app/$$module_name/routes/__init__.py; \
	touch app/$$module_name/routes/$$module_name"_routes.py"; \
	mkdir -p views/$$module_name; \
	mkdir -p tests/$$module_name; \
	touch tests/$$module_name/conftest.py; \
	touch tests/$$module_name/"test_"$$module_name"routes.py"; \
	touch tests/$$module_name/"test_"$$module_name"controllers.py"; \
	touch tests/$$module_name/"test_"$$module_name"repositories.py"; \
	touch tests/$$module_name/"test_"$$module_name"models.py"; \
	echo "Módulo criado com sucesso!"
# pyCBPE

O pyCBPE é um framework desenvolvido para o estudo de aplicações de algoritmos de aprendizagem de máquina para a
estimativa da pressão arterial por meio de sinais de fotopletismografia.

# Pré-requisitos

Para utilizar o framework, é necessário que se tenham os seguintes pré-requisitos configurados na sua máquina:

- [Python 3.8](https://www.python.org/downloads/release/python-380/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [venv](https://docs.python.org/3/library/venv.html)
- [Make](https://www.gnu.org/software/make/)

# Preparação

Para utilizar este projeto, é necessário instalar as suas dependências, como forma de simplificar esse processo, foi
desenvolvido um `Makefile`.

## Clonando o repositório

Para clonar o repositório do projeto e ir para sua pasta, utilize os seguintes comandos:

```bash
cd ~/Documents/
git clone git@github.com:luigiluz/pyCBPE.git
cd pyCBPE/
```

## Instalação

Após instalar os pré-requisitos e clonar o repositório, é necessário instalar as dependências do projeto. Para instalar
as dependências, basta utilizar o seguinte comando:

```bash
$ make bootstrap
```

### Guia de uso

#### Obtenção da base de dados

Para fazer o download da base de dados, basta executar o seguinte comando:

```bash
$ cd files/dataset/
$ wget https://archive.ics.uci.edu/ml/machine-learning-databases/00340/data.zip
$ unzip data.zip
$ cd ../..
```

Talvez seja necessário instalar o pacote unzip para extrair o arquivo da base de dados.

#### Configurar o diretório raiz do projeto

O diretório raiz do projeto é utilizado para gerar os arquivos de base de dados ao longo do projeto, dessa forma,
deve-se atualizar a constante ROOT_PATH do arquivo constants.py com o diretório raiz no qual o diretório se encontra
no seu computador.

#### Preparação da base de dados

Para preparar a base de dados, basta executar o comando abaixo:

```bash
$ make prepare_dataset
```

#### Gerar o dataset de features e labels

Para gerar o dataset de features e labels, basta executar o comando abaixo:

```bash
$ make generate_dataset
```

#### Gerar e avaliar modelo de aprendizagem de máquina

Para gerar e avaliar um dos modelos de aprendizagem de máquina, basta executar um dos comandos abaixo:

```bash
$ make generate_linear_regression_model
```

```bash
$ make generate_decision_tree_model
```

```bash
$ make generate_random_forest_model
```

```bash
$ make generate_adaboost_model
```

No diretório `files/estimators` irá existir uma pasta que contém todas as métricas de avaliação do modelo que foi gerado, bem como o arquivo `.joblib` com o modelo treinado gerado.

#### Limpeza

Para deletar os arquivos criados pelo venv, basta executar o comando abaixo:

```bash
$ make clean
```
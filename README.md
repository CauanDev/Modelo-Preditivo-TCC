# Modelo Preditivo de Mortalidade Infantil – TCC

Este repositório contém todos os códigos e scripts desenvolvidos durante o Trabalho de Conclusão de Curso (TCC) com o objetivo de criar um **modelo preditivo de mortalidade infantil** utilizando técnicas de Machine Learning. O projeto foi estruturado em módulos, sendo que o primeiro passo consiste em **importar a base de dados**, processar os arquivos e preparar os dados para análise.

Além disso, neste repositório estão disponíveis os gráficos utilizados para analisar a coleta de dados, que foram desenvolvidos em React para melhor visualização e interação.

## Pré-requisitos

Antes de iniciar, certifique-se de ter:

- Python 3.10 ou superior instalado.
- `pip` atualizado.
- PostgreSQL rodando localmente ou remotamente.
- Todos os arquivos CSV de 1980 a 2024 (usados na pesquisa) na pasta `arquivos`.
- Node.js e npm (para rodar a aplicação React dos gráficos).
- React e suas dependências instaladas via npm.

O projeto já conta com um **requirements.txt** completo para instalação das dependências Python.

## Estrutura das tabelas no banco de dados

As tabelas utilizadas ao longo do projeto são as seguintes:

- **novos_pacientes**

```sql
    CREATE TABLE public.novos_pacientes (
        contador serial4 NOT NULL,
        nome varchar(50) NULL,
        "natural" varchar(50) NULL,
        dtnasc date NULL,
        sexo varchar(20) NULL,
        racacor varchar(20) NULL,
        codmunocor varchar(50) NULL,
        idademae int4 NULL,
        idade varchar(10) NULL,
        escmae varchar(50) NULL,
        ocupmae varchar(100) NULL,
        peso float8 NULL,
        resultado varchar(15) NULL,
        CONSTRAINT novos_pacientes_pkey PRIMARY KEY (contador)
    );
```


- **obitos_infantil**

```sql

CREATE TABLE public.obitos_infantil (
    contador serial4 NOT NULL,
    "natural" varchar(50) NULL,
    dtnasc date NULL,
    sexo varchar(20) NULL,
    racacor varchar(20) NULL,
    codmunocor varchar(50) NULL,
    idademae int4 NULL,
    idade varchar(10) NULL,
    escmae varchar(50) NULL,
    ocupmae varchar(100) NULL,
    peso float8 NULL,
    CONSTRAINT obitos_infantil_pkey PRIMARY KEY (contador)
);

```

- **sobreviventes**

```sql
    CREATE TABLE public.sobreviventes (
    contador serial4 NOT NULL,
    "natural" varchar(50) NULL,
    dtnasc date NULL,
    sexo varchar(10) NULL,
    idade varchar(10) NULL,
    racacor varchar(20) NULL,
    codmunocor varchar(50) NULL,
    idademae int4 NULL,
    escmae varchar(50) NULL,
    ocupmae varchar(100) NULL,
    peso float8 NULL,
    CONSTRAINT sobreviventes_pkey PRIMARY KEY (contador)
);
```

# Procedimento de Importação da Base de Dados

## Passo 1: Criar e ativar o ambiente virtual

Para garantir isolamento das dependências, recomenda-se utilizar um ambiente virtual:

### Criar ambiente virtual

```bash
python -m venv venv
```

### Ativar o ambiente virtual

**No Linux/macOS:**  
```bash
source venv/bin/activate
```

**No Windows:**  
```bash
venv\Scripts\activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```


## Passo 2: Configurar o banco de dados

O script principal para importação da base é o \`importar_base.py\`. Antes de rodá-lo, configure a conexão com o banco PostgreSQL:

```python
import os
import psycopg2

conexao = psycopg2.connect(
    host="",        # Endereço do servidor PostgreSQL
    database="",    # Nome do banco de dados
    user="postgres",# Usuário
    password="postgres", # Senha
    port=5432       # Porta padrão
)

cursor = conexao.cursor()
```


## Passo 3: Inserir os arquivos CSV

Coloque todos os arquivos CSV utilizados (de 1980 a 2024) na pasta:

\`arquivos/\`

No script, defina o caminho onde os arquivos estão localizados:

```python
caminho_base = os.path.join(os.path.dirname(__file__), '..', 'arquivos')
```

## Observações

- A pesquisa abrange dados do ano de 1980 até 2024.
- Após configurar o banco de dados, é necessário criar as tabelas conforme a estrutura mostrada acima antes de rodar os scripts de importação.

## Passo 4: Executar o script importar_base.py

Antes de executar o script, certifique-se de que todas as tabelas do banco de dados foram criadas conforme os DDLs fornecidos nos passos anteriores.

### Executar o script

Com o ambiente virtual ativado e as dependências instaladas, execute:

```bash
python importar_base.py
```

O script irá importar os dados dos arquivos CSV para as tabelas correspondentes no banco PostgreSQL.

# Procedimento de Treinamento do Modelo Preditivo

O script responsável pelo treinamento do modelo preditivo é o \`treinar_modelo.py\`.

Antes de rodá-lo, configure a conexão com o banco PostgreSQL:

```python
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/db_tcc")
```

Observações importantes:

- Certifique-se de substituir os parâmetros da conexão (`user`, `password`, `host`, `port` e `database`) de acordo com o seu ambiente.
- Antes de executar o script, verifique se todas as tabelas necessárias foram criadas e populadas conforme os passos anteriores, principalmente `obitos_infantil` e `sobreviventes`.
- Com a conexão configurada e as tabelas prontas, você poderá executar o treinamento do modelo com segurança.

## Executar o script

Com o ambiente virtual ativado e as dependências instaladas, execute:

```bash
python treinar_modelo.py
```

O script irá treinar um modelo de Random Forest utilizando os dados do banco PostgreSQL e salvará o modelo, o scaler e as colunas utilizadas nos arquivos correspondentes.

# Procedimento de Análise de Novos Casos

O script responsável por analisar novos pacientes é o \`analisar_casos.py\`.

Antes de rodá-lo, configure a conexão com o banco PostgreSQL:

```python
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/db_tcc")
```

Antes de executar o script, certifique-se de que:

- O modelo preditivo já foi treinado e os arquivos \`random_forest_model.pkl\`, \`scaler.pkl\` e \`model_columns.pkl\` foram gerados.
- Certifique-se de substituir os parâmetros da conexão (`user`, `password`, `host`, `port` e `database`) de acordo com o seu ambiente.
- A tabela \`novos_pacientes\` no banco de dados PostgreSQL está populada com os registros a serem analisados.

## Executar o script

Com o ambiente virtual ativado e as dependências instaladas, execute:

```bash
python analisar_casos.py
```

O script irá:

- Carregar o modelo treinado, o scaler e as colunas utilizadas no treinamento.
- Consultar os novos pacientes da tabela \`novos_pacientes\`.
- Pré-processar os dados para alinhar com o modelo.
- Calcular e exibir a probabilidade de óbito para cada paciente listado.



# Visualização de Gráficos


Para visualizar os gráficos do projeto, você precisará de algumas ferramentas instaladas:

1. **TensorBoard** – para acompanhar métricas do treinamento do modelo.  
   - Pode ser instalado via pip:  
   ```bash
   pip install tensorboard
   ```

2. **Node.js e npm** – para executar a aplicação React que utiliza ApexCharts.  
   - Baixe e instale a partir do site oficial: [https://nodejs.org/](https://nodejs.org/)  
   - Após a instalação, verifique com:  
   ```bash
   node -v
   npm -v
   ```


O projeto gera gráficos de duas formas principais:

1. **TensorBoard** – utilizado para acompanhar métricas do treinamento do modelo.
2. **React/ApexCharts** – utilizado para exibir dashboards interativos na aplicação web.

## TensorBoard

O TensorBoard salva os logs na pasta:

```
logs/random_forest
```

### Executar TensorBoard

No ambiente virtual ativado, execute:

```bash
tensorboard --logdir logs/random_forest --port 6006
```

Em seguida, abra o navegador e acesse:

```
http://localhost:6006
```

Lá você poderá visualizar métricas como ROC AUC, parâmetros testados e evolução do treinamento.

## React/ApexCharts

Os gráficos interativos da aplicação web estão localizados na pasta:

```
graficos/
```

Eles utilizam **React** e **ApexCharts** para renderização.

### Executar a aplicação React

1. Instale as dependências (a partir da pasta \`graficos/\`):

```bash
npm install
```

2. Execute o servidor de desenvolvimento:

```bash
npm start
```

A aplicação será iniciada geralmente em:

```
http://localhost:3000
```

Os gráficos mostrarão as métricas e análises já calculadas pelo backend, de forma interativa e dinâmica.
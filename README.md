# Sistema_aeroporto

Projeto Desenvolvido na matéria PCS3643 - Laboratório de Engenharia de Software I (2022)

---

# Pré-requisitos

- `Python`
- `Django`

# Instalando Pré-requisito Python

 - Faça o download do [Python](https://www.python.org/downloads/)

- Instale em sua máquina e marque a opção de adiocinar o python ao Path.


# Instalando Projeto

1) git clone nesse repositório

2) Navegue até

```bash
\sistema_aeroporto\webapp
```

# Criando ambiente virtual (env)

- Use

```bash
python -m venv env
```

# Ativando ambiente virtual

- Use

```bash
.\env\scripts\activate.ps1
```

---
Tente isso caso o comando acima não funcionar:

```bash
.\env\bin\activate.ps1
```

---

Tente isso também caso o comando acima não funcione:

```bash
.\venv\Scripts\Activate.ps1
```

# Executando aplicação

### Use URL do endereço da aplicação 

```bash
pmarq98.pythonanywhere.com

```
## Pronto, você será direcionado para página Login, agora é só testar!

---

# Rodando Testes


Navegue até

```bash
\sistema_aeroporto\webapp\MyProj
```

- Note que haverá um arquivo chamado ``` manage.py ```

- Vamos criar do banco de dados a partir do modelo (migration)

### Use

```bash
python manage.py makemigrations
```

---

## Para criar o banco execute:

```bash
python manage.py migrate
```

## Caso ocorra algum problema com a criação do banco

### Use

```bash
 python manage.py migrate --run-syncdb
```


---

## Executando Testes:

```bash
python manage.py test
```

# Visualização do  Banco de dados

- Utilize alguma extenção do VScode como SQlite ou algum programa como DBeaver e visualize suas tabelas.

---

# Navegando no Sistema

## Tela de login

- Usuários cadastrados: operador 1234,
                        funcionario 1234,
                        torre 1234,
                        piloto 1234,
                        gerente 1234,
  cada um com funções específicas

---

## Tela Home

- Você encontrará a Dashboard, uma tela onde estará disponível os dez últimos voos em andamento.

---

## Tela de cadastro

- Na tela do cadastro, preencha as lacunas com as informações do voo e confirme a inserção de um novo voo.

---

## Tela de Listar Voo
- Todos os campos são modos de filtragem para facilitar a localização do voo espefífico. Rolando a página para baixo, terá uma lista com todos os voos.

---

## Tela de Monitoração
- Todos os campos são modos de filtragem para facilitar a localização do voo espefífico. Rolando a página para baixo, terá uma lista com todos os voos, podendo alterar a data e horário de partida ou de chegada

---

## Tela de Gerar Relatório
- Nessa tela, você tera 4 opções de relatório em nosso sistema, escolha a opção desejada e exporte para um arquivo PDF.

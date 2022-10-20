# Sistema_aeroporto

Projeto Desenvolvido na matéria PCS3643 - Laboratório de Engenharia de Software I (2022)

---

# Pré-requisitos

- `Python`
- `Django`

# Instalando Pré-requisito Python

 - Faça o download do [Python](https://www.python.org/downloads/)

- Instale em sua máquina e marque a opção de adiocinar o python ao Path.

# Instalando Pré-requisito Django

- Use
 
 ```bash
pip install django
```

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

Navegue até

```bash
\sistema_aeroporto\webapp\MyProj
```

---


Vamos certificar que o pré-requisisto `Django` está instalado:

Use

 ```bash
pip install django
```
---


Vamos executar a aplicação:


Use

```bash
ls
```
Tente isso caso o comando acima não funcionar:

```bash
dir
```

---

- Note que haverá um arquivo chamado ``` manage.py ```

### Use

```bash
python manage.py runserver
```

- Note que será informado uma URL do endereço da aplicação 

### Cole no navegador
```bash
http://127.0.0.1:8000/

```
## Pronto, você será direcionado para página Home, agora é só testar!

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

---

## Executando Testes:

```bash
python manage.py test
```

# Visualização do  Banco de dados

- Utilize alguma extenção do VScode como SQlite ou algum programa como DBeaver e visualize suas tabelas.

## Tudo certo? Até a próxima!
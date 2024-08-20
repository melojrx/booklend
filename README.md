# Booklend 

Projeto de Gerenciamento de Empréstimo de Livros para Bibliotecas. 

## Requisitos

Certifique-se de que você tenha os seguintes requisitos instalados em seu sistema:

- Python (versão recomendada: 3.10 ou superior)
- Django (instalado automaticamente ao seguir as instruções abaixo)
- Outras dependências listadas no arquivo `requirements.txt`


## Instalação das Dependências

Com o ambiente virtual ativado, instale as dependências do projeto usando o comando:
```bash
pip install -r requirements.txt
```


## Rodar o projeto

Após instalar as dependências, aplique as migrations no banco de dados com o comando:
```bash
python manage.py migrate
```

Agora o projeto jã pode ser inicializado com o comando:
```bash
python manage.py runserver
```

Após isso, o sistema estará pronto para ser acessado em:
[http://localhost:8000](http://localhost:8000)

---

## Imagens do Projeto

> ### Formulário de Login
![image](/static/img/login.png) 

> ### Formulário de Cadastro de Usuários pelos Admins
![image](static\img\cadastro.png) 

> ### Formulário de Cadastro de Livros
![image](static\img\cadastro_livro.png) 


> ### Dashboard de acompanhamento de Empréstimos
![image](static\img\dashboard.png)


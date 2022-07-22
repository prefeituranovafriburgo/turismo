# Controle de Turismo <br>

> Gerador de senhas para controle de transporte turístico. <br>

<hr>

### Tecnologias
<p>
<img src="https://img.icons8.com/color/48/000000/python.png"/>&nbsp;&nbsp;
<img src="https://img.icons8.com/color/48/000000/django.png"/>&nbsp;&nbsp;
<img src="https://img.icons8.com/color/48/000000/bootstrap.png"/>&nbsp;&nbsp;
<img src="https://img.icons8.com/windows/48/000000/font-awesome.png"/>&nbsp;&nbsp;
<img src="https://img.icons8.com/color/48/000000/maria-db.png"/>
</p>

### Pré-requisitos
- Versão 3 ou mais recente de Python.
- MariaDB ou MySql




### 1. Instalação de dependências

Para instalar as dependências do projeto basta usar o comando:<br>
`pip install -r requeriments.txt`

Ou instale os módulos abaixo:

- asgiref==3.4.1
- certifi==2021.10.8
- cffi==1.15.0
- charset-normalizer==2.0.12
- cryptography==36.0.2
- defusedxml==0.7.1
- Django==3.2.10
- django-qr-code==2.3.0
- django-recaptcha==3.0.0
- idna==3.3
- oauthlib==3.2.0
- pycparser==2.21
- PyJWT==2.3.0
- PyMySQL==1.0.2
- python3-openid==3.2.0
- pytz==2021.3
- requests==2.27.1
- requests-oauthlib==1.3.1
- segno==1.4.1
- semantic-version==2.9.0
- setuptools-rust==1.1.2
- social-auth-app-django==5.0.0
- social-auth-core==4.2.0
- sqlparse==0.4.2
- typing_extensions==4.0.1
- urllib3==1.26.8


### 2. Configurações
#### Configurando as variáveis de ambiente.

Para criar as variáveis de ambiente crie um arquivo com o nome `.envars.yaml` na raiz do seu projeto ou no diretório **acima da pasta do seu projeto** contendo as seguintes informações conforme o modelo abaixo:
```
db_name: nomedobanco # Este projeto foi pensando para suportar MySql ou MariaDB
db_user: usuariodobanco # Usuário do banco com todas as permissões para a base de dados
db_pw: senhadobanco # A senha do respectivo usuário do banco
django_secret_key: secretkey123456 # Insira sua django secret key
debug_mode: True # Use True para DEBUG or False para PRODUCTION
email_sistema: seu@email.com # E-mail utilizado para recuperação de senha
email_pw: su@senha123 # Senha do email acima
hCAPTCHA_Public_Key: 6484-dsadad4994ds949494d2314 # Inscreva-se https://www.hcaptcha.com/
hCAPTCHA_Secret_Key: 6484-dsadad4994ds949494d2314dsd4900c0952 # Cadastre seu site após se inscrever
GOOGLE_OAUTH2_PUBLIC_KEY: 74526484-dsadad4994ds949494d2314.apps.googleusercontent.com # Inscreva-se https://console.cloud.google.com/ e gere as chames para seu site
GOOGLE_OAUTH2_SECRET_KEY: GOCSPX-dsadad4994ds949494d2314
FACEBOOK_DEVELOPER_PUBLIC_KEY: 4994ds949494d2314 # Inscreva-se https://developers.facebook.com/ e gere as chaves para seu site
FACEBOOK_DEVELOPER_SECRET_KEY: 494d231479ff65cb6307b3
```

------------


### 3.Usando o projeto
Para utilizar o projeto, você precisa criar um usuário utilizando o seguinte comando: <br>
`python manage.py createsuperuser`  <br>
No campo de usuário, você **deverá** informar o seu **e-mail**. As credenciais (e-mail e senha) serão utilizadas para realizar o login no site.

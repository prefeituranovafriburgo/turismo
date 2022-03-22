# Turismo
Gerador de senhas para controle de transporte turístico

## Instalação

Para instalar as dependencias do projeto basta usar o comando: **pip install -r requeriments.txt**

## Configurando as Variáveis de Ambiente

Para criar as variáveis de ambiente crie um arquivo com o nome **'.envars.yaml'** na raiz do seu projeto ou no diretrio **acima da pasta do seu projeto** contendo as seguintes informações conforme o modelo abaixo:
```
>db_name: turismo # Este projeto foi pensando para suportar MySql ou MariaDB
>db_user: usuariodobanco # Usuário do banco com todas as permissões para a base de dados
>db_pw: senhadobanco # A senha do respectivo usuário do banco
>django_secret_key: turismo@sme.novafriburgo.rj.gov.br123456 # Insira sua django secret key
>debug_mode: True # Use True para DEBUG or False para PRODUCTION
>email_sistema: senhas_turismo@sme.novafriburgo.rj.gov.br # E-mail utilizado para recuperação de senha
>email_pw: nU2Ke=u%45621 # Senha do email acima
>hCAPTCHA_Public_Key: 6730e60d-fdfb-462a-b60e-a6478a3006f2 # Inscreva-se https://www.hcaptcha.com/
>hCAPTCHA_Secret_Key: 0x83eE0d7d855633562B0333b715839DA6600c0952 # Cadastre seu site após se inscrever
>GOOGLE_OAUTH2_PUBLIC_KEY: 745294971401-qso3hr2ioa2pgqd45t6ab4dvi4ip2297.apps.googleusercontent.com # Inscreva-se https://console.cloud.google.com/ e gere as chames para seu site
>GOOGLE_OAUTH2_SECRET_KEY: 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
>FACEBOOK_DEVELOPER_PUBLIC_KEY: 1840522456142106 # Inscreva-se https://developers.facebook.com/ e gere as chaves para seu site
>FACEBOOK_DEVELOPER_SECRET_KEY: 388ee4b6d1089ead679ff65cb6307b3
```
# Turismo
Gerador de senhas para controle de transporte turístico

# ===========================

Instruções
Para instalar QR Code, usar: pip install django-qr-code
https://django-qr-code.readthedocs.io/en/latest/pages/README.html

# ===========================

Para criar as variáveis de ambiente, criar arquivo com nome .envvar
no diretório imediatamente acima da pasta raiz do sistema, com o
seguinte conteúdo:

----------------------------------
nome_banco_de_dados

usuário_banco_de_dados

senha_banco_de_dados

secret_key_do_arquivo_settings.py

True

turismo@sme.novafriburgo.rj.gov.br

senhaemail
----------------------------------

Explicação do arquivo acima:
- linha 1: nome do banco de dados;
- linha 2: usuário do banco de dados;
- linha 3: senha do banco de dados;
- linha 4: secret key usado no arquivo settings.py;
- linha 5: Conteúdo da variável DEBUG no arquivo settings.py. Deixar True para poder receber mensagens de erro;
- linha 6: e-mail utilizado para serviços como recuperação de senha. Só há necessidade de colocar e-mail real se for testar a parte de recuperação de senhas;
- linhs 7: senha do e-mail. Só há necessidade de colocar e-mail real se for testar a parte de recuperação de senhas.

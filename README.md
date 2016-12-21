# Configuração 


- configure o servidor mysql para conexões vias SSL:
  http://xmodulo.com/enable-ssl-mysql-server-client.html
  
  
- mova 'client-cert.pem' e 'client-key.pem' para o diretório SSLcertificate/dbSite/


- gere um certificado SSL auto-assinado:

    openssl genrsa -des3 -out server.orig.key 2048
    
    openssl rsa -in server.orig.key -out server.key
    
    openssl req -new -key server.key -out server.csr
    
    openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
    
  
  
- mova 'server.crt' e 'server.key' para o diretório SSLcertificate/sistema/
 
# Como usar


- python System.py


- python Client.py <cliente> <senha>

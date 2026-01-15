FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y nginx openssl

# 1. Config OpenSSL pour charger le provider "legacy" (indispensable en 2026)
RUN printf "openssl_init = openssl_init_sect\n\
[openssl_init_sect]\n\
providers = provider_sect\n\
[provider_sect]\n\
default = default_sect\n\
legacy = legacy_sect\n\
[default_sect]\n\
activate = 1\n\
[legacy_sect]\n\
activate = 1\n" > /etc/ssl/openssl.cnf

# 2. Baisser le niveau de sécurité global
RUN echo "[system_default_sect]\nMinProtocol = TLSv1\nCipherString = DEFAULT@SECLEVEL=0" >> /etc/ssl/openssl.cnf

# 3. Certificat et Config Nginx avec Ciphers explicites
RUN openssl req -x509 -nodes -newkey rsa:2048 -keyout /k.key -out /c.crt -subj "/CN=localhost"
RUN echo 'server { \
    listen 443 ssl; \
    ssl_certificate /c.crt; \
    ssl_certificate_key /k.key; \
    ssl_protocols TLSv1; \
    ssl_ciphers "DEFAULT:@SECLEVEL=0"; \
    location / { \
        default_type text/plain; \
        return 200 "CONNEXION TLS 1.0 REUSSIE\nFelicitations, le serveur est vulnerable."; \
    } \
}' > /etc/nginx/sites-enabled/default

CMD ["nginx", "-g", "daemon off;"]

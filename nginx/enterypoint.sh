# nginx/entrypoint.sh
#!/bin/sh
if [ ! -f /etc/letsencrypt/live/glasshalf.ru/fullchain.pem ]; then
  certbot certonly \
    --webroot -w /var/www/certbot \
    --non-interactive --agree-tos \
    -m you@your-email.com \
    -d glasshalf.ru -d www.glasshalf.ru
fi
nginx -g 'daemon off;'

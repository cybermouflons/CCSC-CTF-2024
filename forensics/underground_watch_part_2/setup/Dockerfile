FROM php:7.4-apache

RUN apt-get update && apt-get install -y socat netcat net-tools

WORKDIR /var/www/html

COPY css css
COPY fonts fonts
COPY images images
COPY js js
COPY uploads uploads
COPY index.php index.php
COPY upload.php upload.php

# Populate challenge with orion_shell
COPY bot_commands/orion_shell.php uploads/orion_shell.php 

RUN chown -R www-data:www-data /var/www/html

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Populate challenge with certificate file
COPY bot_commands/certificate.pem /var/log/apache2/.project-echo.pem
RUN chown www-data:www-data /var/log/apache2/.project-echo.pem


ENTRYPOINT ["/entrypoint.sh"]
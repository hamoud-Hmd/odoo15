FROM odoo:15.0
WORKDIR /mnt/my-addons
COPY addons/ .
WORKDIR /etc/odoo
COPY config/odoo.conf odoo.conf
EXPOSE 8069

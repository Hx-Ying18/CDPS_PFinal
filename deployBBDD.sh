#!/usr/bin/env bash

apt update
apt -y install mariadb-server
sed -i -e 's/bind-adress.*/bind-adress=0.0.0.0/' -e 's/utf8mb4/utf8/' /etc/mysql/mariadb.conf.d/50-server.cnf
systemctl restart mysql

mysqladmin -u root password xxxx
mysql -u root --password='xxxx' -e "CREATE USER 'quiz' IDENTIFIED BY 'xxxx';"
mysql -u root --password='xxxx' -e "CREATE DATABASE quiz;"
mysql -u root --password='xxxx' -e "GRANT ALL PRIVILEGES ON quiz.* to 'quiz'@'%' IDENTIFIED BY 'xxxx';"
mysql -u root --password='xxxx' -e "FLUSH PRIVILEGES;"


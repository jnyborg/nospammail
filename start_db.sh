#!/bin/bash
NAME=nospammail-db
docker stop $NAME && docker rm $NAME

docker run --name watchmedier-top-news -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password -d mysql:5

sleep 20
#create database
docker exec -i watchmedier-top-news /bin/bash -c "mysql -u root '-ppassword' -e 'CREATE DATABASE top_news CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;' "
docker exec -i watchmedier-top-news /bin/bash -c "mysql -u root '-ppassword' -e 'CREATE DATABASE top_news_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;' "

SQL=$(cat src/main/resources/create.sql)

docker exec -i watchmedier-top-news /bin/bash -c "mysql -u root '-ppassword' -e 'use top_news; $SQL'"
echo "Database started"

#!/usr/bin/env bash

cd /root/quiz_2019
mkdir public/uploads
npm install
npm install forever
npm install mysql2
export QUIZ_OPEN_REGISTER=yes
export DATABASE_URL=mysql://quiz:xxxx@10.2.4.31:3306/quiz

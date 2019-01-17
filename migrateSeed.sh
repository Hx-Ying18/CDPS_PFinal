#!/usr/bin/env bash

cd /root/quiz_2019/
export QUIZ_OPEN_REGISTER=yes
export DATABASE_URL=mysql://quiz:xxxx@20.2.4.31:3306/quiz
npm run-script migrate_cdps
npm run-script seed_cdps

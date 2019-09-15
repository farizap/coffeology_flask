#!/bin/bash

sudo docker stop coffeology_flask
sudo docker rm coffeology_flask
sudo docker rmi farizap/coffeology_flask
sudo docker run -d --name coffeology_flask -p 5000:5000 farizap/coffeology_flask:latest

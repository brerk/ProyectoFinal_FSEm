#!/bin/bash

apt-get install virtualenv  -y

# TODO: Enable 1-wire
git clone https://github.com/brerk/ProyectoFinal_FSEm.git
cd ProyectoFinal_FSEm

virtualenv venv

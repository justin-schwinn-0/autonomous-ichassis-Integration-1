#!/bin/bash

git stash clear
git stash
git pull
sudo python3 rpi_chassis.py
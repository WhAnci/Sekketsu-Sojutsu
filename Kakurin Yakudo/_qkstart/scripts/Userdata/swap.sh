#!/bin/bash
# 128 MB * 16 = 2 GB
sudo dd if=/dev/zero of=/swapfile bs=128M count=16
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab
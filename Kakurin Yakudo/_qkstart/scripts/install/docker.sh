#!/bin/bash
sudo dnf install docker -y
sudo systemctl enable --now docker
sudo usermod -aG docker $(whoami)


cat <<EOT >> ~/.bashrc
source /etc/profile.d/bash_completion.sh
EOT

mkdir -p ~/.local/share/bash-completion/completions
docker completion bash > ~/.local/share/bash-completion/completions/docker

mkdir -p ~/.oh-my-zsh/completions
docker completion zsh > ~/.oh-my-zsh/completions/_docker
echo "새 쉘에서 docker를 사용하려면 'newgrp docker' 를 사용하세요."
sudo su $(whoami)

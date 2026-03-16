#!/bin/bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

sudo sh -c 'helm completion bash > /etc/bash_completion.d/helm'
sudo sh -c "helm completion zsh > \"${fpath[1]}/_helm\""

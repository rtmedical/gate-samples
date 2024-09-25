#!/bin/bash
# entrypoint.sh

# Saia imediatamente se algum comando falhar
set -e

# Fonte o arquivo de configuração para configurar o ambiente
source /etc/mybashrc

# Inicie o Jupyter Notebook em segundo plano sem token
jupyter notebook --ip=0.0.0.0 --no-browser --allow-root --NotebookApp.token=''  

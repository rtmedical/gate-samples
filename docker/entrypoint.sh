#!/bin/bash
# entrypoint.sh

# Saia imediatamente se algum comando falhar
set -e



# Inicie o Xvfb em segundo plano
Xvfb :99 -screen 0 1024x768x24 &
export DISPLAY=:99

# Fonte o arquivo de configuração para configurar o ambiente
source /etc/mybashrc

# Habilite as extensões do Jupyter para widgets
jupyter nbextension enable --py widgetsnbextension --sys-prefix
jupyter nbextension enable --py ipympl --sys-prefix

# Inicie o Jupyter Notebook em segundo plano sem token
jupyter notebook --ip=0.0.0.0 --no-browser --allow-root --NotebookApp.token='' &

# Execute o script original para comandos GATE
exec /runGate.sh "$@"

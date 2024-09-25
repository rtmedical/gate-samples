#!/bin/bash
# run_gate.sh

# Saia imediatamente se algum comando falhar
set -e

# Fonte o arquivo de configuração
source /etc/mybashrc

# Execute o Gate com os argumentos fornecidos
Gate "$@"

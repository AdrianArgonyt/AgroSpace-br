## AgroSpace BR

O AgroSpace BR é um MVP (Produto Mínimo Viável) educacional projetado para cadastrar culturas agrícolas e ambientes planetários. O objetivo principal é comparar uma cultura com um ambiente planetário para calcular um score de compatibilidade, listar fatores limitantes e fornecer uma análise com recomendações de ajustes (ex: solo, pressão, água, luz).

Este projeto foi gerado com base em uma especificação detalhada, incluindo um backend em Python/Flask, um banco de dados SQL Server e um frontend em HTML+JS puro.

1. Instalação

Primeiro, certifique-se de que você tem uma versão compatível do Python (3.11 ou 3.12) instalada.

# 1. Crie a estrutura de pastas e coloque os arquivos conforme especificado.
# 2. Navegue até a pasta raiz 'AgroSpace-br' usando o terminal.
cd caminho/para/AgroSpace-br

# 3. Crie um ambiente virtual (Recomendado)
python -m venv .venv

# 4. Ative o ambiente virtual
# No Windows
.venv\Scripts\activate

# 5. Instale os pacotes necessários
pip install -r requirements.txt

# 6. Crie e configure o arquivo .env
# No Windows: copy .env.example .env
# Em seguida, abra o arquivo .env e cole sua string de conexão completa na variável DB_CONN_STR.
# Exemplo: DB_CONN_STR="DRIVER={ODBC Driver 17 for SQL Server};SERVER=seu_servidor;DATABASE=AgroSpaceBR;UID=seu_usuario;PWD=sua_senha"


1.1 Solução de Problemas Comuns

Problema 1: Erro na instalação do pyodbc (Microsoft Visual C++ 14.0 or greater is required)

Este erro acontece porque a pyodbc precisa ser compilada, o que exige as Ferramentas de Build do C++ da Microsoft.

Solução:

Baixe o instalador do "Build Tools for Visual Studio": https://visualstudio.microsoft.com/visual-cpp-build-tools/

Execute o instalador e, na aba "Cargas de trabalho", selecione "Desenvolvimento para desktop com C++".

Após a instalação, reinicie o computador.

Tente executar pip install -r requirements.txt novamente.

Problema 2: Erro de Conexão (...target machine actively refused it ou ...Data source name not found)

Com a nova abordagem, a maioria dos erros de conexão significa que a sua DB_CONN_STR está incorreta ou o servidor SQL não está acessível.

Solução: Verifique sua String de Conexão e o SQL Server

String de Conexão: Verifique cada parte da sua DB_CONN_STR no arquivo .env. Erros de digitação no nome do driver, do servidor ou na senha são muito comuns.

Acesso ao Servidor: Se o erro persistir, abra o SQL Server Configuration Manager na máquina do servidor e garanta que o protocolo TCP/IP para a sua instância do SQL Server esteja Habilitado. Se você alterar, lembre-se de reiniciar o serviço do SQL Server.

Problema 3: Erro "Cannot connect to WMI provider" ao abrir o SQL Server Configuration Manager

Se você não conseguir abrir o Configuration Manager, siga os passos para reparar o provedor WMI.

Solução: Recompilar o Provedor WMI

Abra o PowerShell como Administrador.

Use o comando abaixo para encontrar o arquivo .mof em todo o disco C:\. Atenção: esta busca pode demorar vários minutos.

Get-ChildItem -Path C:\ -Recurse -Filter "sqlmgmproviderxpsp2up.mof" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName


Copie o caminho retornado e use-o no comando mofcomp:

mofcomp "C:\Caminho\Encontrado\Pela\Busca\sqlmgmproviderxpsp2up.mof"


Se o arquivo não for encontrado, a instalação do SQL Server pode estar corrompida e talvez precise ser reparada através de "Adicionar ou remover programas".

2. Configuração do Banco de Dados

Com o arquivo .env configurado, este script irá criar o banco de dados e as tabelas.

# Rode o script de bootstrap do banco de dados (execute apenas uma vez)
python bootstrap/bootstrap_db.py


3. Executando a Aplicação

Modo de Desenvolvimento

# Execute o servidor de desenvolvimento do Flask
flask --app api.app run --debug -p 8114


Acesse em: http://localhost:8114

Modo de Produção

# Execute a aplicação com o waitress
python -m waitress --listen=0.0.0.0:8114 api.app:app


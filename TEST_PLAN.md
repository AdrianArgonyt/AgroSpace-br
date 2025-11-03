# Plano de Testes da Aplicação - AgroSpace BR

## 1. Introdução

Este documento descreve o Plano de Testes para a aplicação **AgroSpace BR**, em conformidade com os requisitos do TP4.  
Os casos de teste são baseados nos Casos de Uso (funcionalidades) definidos no TP2 e expandidos no TP3/TP4.

Para cada Caso de Uso, são detalhados **3 casos de teste (CT)** distintos, cobrindo:
- Caminho feliz (sucesso)
- Caminhos alternativos
- Exceções / erro de validação / restrição de acesso

## 2. Casos de Uso Testados

- UC01: Verificar Saúde do Sistema  
- UC02: Listar Culturas (com filtro)  
- UC03: Listar Ambientes (com filtro)  
- UC04: Realizar Simulação de Compatibilidade  
- UC05: Registar Novo Utilizador  
- UC06: Efetuar Login de Utilizador (Admin)  
- UC07: Aceder ao Painel de Administração (Rota Protegida)  
- UC08: Cadastrar Nova Cultura (Admin)  
- UC09: Cadastrar Novo Ambiente (Admin)  

---

## 3. Casos de Teste Detalhados

### UC01: Verificar Saúde do Sistema

| ID do Teste  | Descrição                         | Passos para Execução                                                                                                                                      | Dados de Entrada      | Resultado Esperado                                                                                                                                             |
|--------------|-----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| UC01-CT01    | Teste de sucesso (caminho feliz)  | 1. Iniciar o servidor de backend.<br>2. Aceder ao endpoint da API.                                                                                        | `GET /api/health`     | Status HTTP `200`.<br>JSON de resposta: `{"status": "ok", "db": {"status": "ok", ...}}`.                                                                        |
| UC01-CT02    | Teste de falha (DB offline)       | 1. Parar o serviço do SQL Server.<br>2. Iniciar o servidor de backend.<br>3. Aceder ao endpoint da API.                                                   | `GET /api/health`     | Status HTTP `503` (Service Unavailable).<br>JSON de resposta: `{"status": "degraded", "db": {"status": "degraded"}}`.                                          |
| UC01-CT03    | Método não permitido              | 1. Iniciar o servidor.<br>2. Enviar uma requisição **POST** para o endpoint de health.                                                                    | `POST /api/health`    | Status HTTP `405` (Method Not Allowed).                                                                                                                        |

---

### UC02: Listar Culturas

| ID do Teste  | Descrição                      | Passos para Execução                                                                                                                                  | Dados de Entrada                      | Resultado Esperado                                                                                                                                              |
|--------------|--------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| UC02-CT01    | Listar todas as culturas       | 1. Iniciar o servidor (com o banco de dados populado).<br>2. Aceder ao endpoint.                                                                      | `GET /api/crops`                      | Status HTTP `200`.<br>JSON de resposta: Array `[...]` contendo objetos de cultura (ex: `"Mandioca"`, `"Batata-doce"`).                                          |
| UC02-CT02    | Filtrar cultura existente      | 1. Iniciar o servidor.<br>2. Aceder ao endpoint com parâmetro de query.                                                                               | `GET /api/crops?q=Mandioca`           | Status HTTP `200`.<br>JSON de resposta: Array `[...]` contendo apenas a cultura `"Mandioca"`.                                                                   |
| UC02-CT03    | Filtrar cultura inexistente    | 1. Iniciar o servidor.<br>2. Aceder ao endpoint com parâmetro de query.                                                                               | `GET /api/crops?q=Alface`             | Status HTTP `200`.<br>JSON de resposta: Array vazio `[]`.                                                                                                       |

---

### UC03: Listar Ambientes

| ID do Teste  | Descrição                        | Passos para Execução                                                                                                                                  | Dados de Entrada                              | Resultado Esperado                                                                                                                                              |
|--------------|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| UC03-CT01    | Listar todos os ambientes        | 1. Iniciar o servidor (com o banco de dados populado).<br>2. Aceder ao endpoint.                                                                      | `GET /api/environments`                       | Status HTTP `200`.<br>JSON de resposta: Array `[...]` contendo objetos de ambiente (ex: `"Marte"`, `"Lua"`, `"ISS"`).                                           |
| UC03-CT02    | Filtrar ambiente existente       | 1. Iniciar o servidor.<br>2. Aceder ao endpoint com parâmetro de query.                                                                               | `GET /api/environments?q=Marte`               | Status HTTP `200`.<br>JSON de resposta: Array `[...]` contendo apenas o ambiente `"Marte"`.                                                                     |
| UC03-CT03    | Filtrar ambiente inexistente     | 1. Iniciar o servidor.<br>2. Aceder ao endpoint com parâmetro de query.                                                                               | `GET /api/environments?q=Plutão`              | Status HTTP `200`.<br>JSON de resposta: Array vazio `[]`.                                                                                                       |

---

### UC04: Realizar Simulação de Compatibilidade

| ID do Teste  | Descrição                         | Passos para Execução                                                                                                                                                                                                                                                | Dados de Entrada                                                                                              | Resultado Esperado                                                                                                                                                                             |
|--------------|-----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| UC04-CT01    | Teste de compatibilidade alta     | 1. Carregar a UI.<br>2. Selecionar `"Batata-doce"`.<br>3. Selecionar `"Estação Espacial (ISS)"`.<br>4. Clicar em `"Combinar"`.                                                                                                                                        | `POST /api/match`<br>Body: `{"cropId": 2, "environmentId": 6}` (IDs válidos)                                   | Status HTTP `200`.<br>JSON de resposta: `{"score": >70, ...}`.<br>A UI exibe a tela de Resultado.                                                                                              |
| UC04-CT02    | Teste de compatibilidade baixa    | 1. Carregar a UI.<br>2. Selecionar `"Mandioca"`.<br>3. Selecionar `"Vénus"`.<br>4. Clicar em `"Combinar"`.                                                                                                                                                           | `POST /api/match`<br>Body: `{"cropId": 4, "environmentId": 5}` (IDs válidos)                                   | Status HTTP `200`.<br>JSON de resposta: `{"score": <20, ...}`.<br>A UI exibe Resultado com vários Fatores Limitantes.                                                                          |
| UC04-CT03    | Teste com dados inválidos         | 1. Enviar requisição para a API com um ID inexistente.                                                                                                                                                                                                             | `POST /api/match`<br>Body: `{"cropId": 999, "environmentId": 1}`                                               | Status HTTP `404` (Not Found).<br>JSON de resposta: `{"error": "Cultura ou Ambiente não encontrado."}`.                                                                                         |

---

### UC05: Registar Novo Utilizador

| ID do Teste  | Descrição                              | Passos para Execução                                                                                                                                                     | Dados de Entrada                                                                                                    | Resultado Esperado                                                                                                                                                        |
|--------------|----------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| UC05-CT01    | Registar novo utilizador (sucesso)     | 1. Navegar para a tela de Login.<br>2. Clicar em `"Registar"`.<br>3. Preencher e submeter o formulário.                                                                   | `POST /api/register`<br>Body: `{"username": "novo_user", "password": "password123"}`                                 | Status HTTP `201`.<br>JSON de resposta: `{"message": "Usuário registrado com sucesso."}`.                                          |
| UC05-CT02    | Registar utilizador existente          | 1. Submeter o formulário de registo com um utilizador que já existe (ex: `"admin"`).                                                                                     | `POST /api/register`<br>Body: `{"username": "admin", "password": "password123"}`                                     | Status HTTP `409` (Conflict).<br>JSON de resposta: `{"error": "Este nome de usuário já está em uso."}`.                            |
| UC05-CT03    | Registar com senha curta               | 1. Submeter o formulário de registo com uma senha inválida (curta demais).                                                                                               | `POST /api/register`<br>Body: `{"username": "user_novo_2", "password": "123"}`                                      | Status HTTP `400` (Bad Request).<br>JSON de resposta: `{"error": "A senha deve ter pelo menos 6 caracteres."}`.                    |

---

### UC06: Efetuar Login de Utilizador (Admin)

| ID do Teste  | Descrição                        | Passos para Execução                                                                                                                                                                        | Dados de Entrada                                                                                              | Resultado Esperado                                                                                                                                                                                                 |
|--------------|----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| UC06-CT01    | Login com sucesso (admin)        | 1. Navegar para a tela de Login Admin.<br>2. Preencher e submeter o formulário de login.                                                                                                    | `POST /api/login`<br>Body: `{"username": "admin", "password": "admin"}`                                        | Status HTTP `200`.<br>JSON de resposta: `{"token": "...", "user": {"username": "admin", "isAdmin": true}}`.<br>A UI navega automaticamente para a tela Admin.                                                     |
| UC06-CT02    | Login com senha incorreta        | 1. Preencher o formulário com a senha errada.                                                                                                                                                | `POST /api/login`<br>Body: `{"username": "admin", "password": "senhaerrada"}`                                  | Status HTTP `401` (Unauthorized).<br>JSON de resposta: `{"error": "Credenciais inválidas."}`.                                                                              |
| UC06-CT03    | Login com utilizador inexistente | 1. Preencher o formulário com um utilizador que não existe.                                                                                                                                 | `POST /api/login`<br>Body: `{"username": "naoexiste", "password": "admin"}`                                    | Status HTTP `401` (Unauthorized).<br>JSON de resposta: `{"error": "Credenciais inválidas."}`.                                                                              |

---

### UC07: Aceder ao Painel de Administração (Rota Protegida)

| ID do Teste  | Descrição                                          | Passos para Execução                                                                                                                                                                                                 | Dados de Entrada       | Resultado Esperado                                                                                                                                          |
|--------------|----------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| UC07-CT01    | Aceder à tela Admin (autenticado)                  | 1. Fazer login como Admin.<br>2. Clicar no botão `"Admin"` na navegação.                                                                                                                                             | N/A (Acesso via UI)    | A UI renderiza a tela de Administração (`view-admin`) com os formulários de cadastro.                                                                      |
| UC07-CT02    | Tentar aceder à tela Admin (sem login)             | 1. Abrir a aplicação (sem login).<br>2. Tentar navegar diretamente para a tela de Admin (ex: manipulando a rota no frontend).                                                                                       | N/A (Acesso via UI)    | A aplicação redireciona automaticamente o utilizador para a tela de Login (`view-login`).                                                                  |
| UC07-CT03    | Tentar aceder após Logout                          | 1. Fazer login como Admin.<br>2. Fazer logout.<br>3. Tentar aceder novamente ao painel Admin.                                                                                                                        | N/A (Acesso via UI)    | A aplicação redireciona o utilizador para a tela de Login.                                                                                                  |

---

### UC08: Cadastrar Nova Cultura (Admin)

| ID do Teste  | Descrição                                   | Passos para Execução                                                                                                                                                                                                                         | Dados de Entrada                                                                                                         | Resultado Esperado                                                                                                                                                                             |
|--------------|---------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| UC08-CT01    | Cadastrar cultura (sucesso)                  | 1. Fazer login como Admin.<br>2. Preencher o formulário `"Cadastrar Nova Cultura"` com dados válidos.<br>3. Submeter.                                                                                                                        | `POST /api/crops` (com Token)<br>Body: `{"CommonName": "Milho", "TempMinC": 18, ...}`                                    | Status HTTP `201`.<br>JSON de resposta: objeto da nova cultura criada.<br>A UI exibe mensagem de sucesso.                                              |
| UC08-CT02    | Tentar cadastrar (sem login)                 | 1. Tentar enviar a requisição de cadastro sem um Token de autenticação.                                                                                                                               | `POST /api/crops` (sem Token)<br>Body: `{"CommonName": "Milho", ...}`                                                    | Status HTTP `401` (Unauthorized).<br>JSON de resposta: `{"error": "Token de autenticação ausente."}`.                                                   |
| UC08-CT03    | Tentar cadastrar (dados inválidos)           | 1. Fazer login como Admin.<br>2. Submeter o formulário de cultura **sem** o campo obrigatório `CommonName`.                                                                                           | `POST /api/crops` (com Token)<br>Body: `{"TempMinC": 18, ...}`                                                           | Status HTTP `400` (Bad Request).<br>JSON de resposta: `{"error": "O campo 'CommonName' é obrigatório."}`.                                              |

---

### UC09: Cadastrar Novo Ambiente (Admin)

| ID do Teste  | Descrição                                   | Passos para Execução                                                                                                                                                                                                                         | Dados de Entrada                                                                                                              | Resultado Esperado                                                                                                                                                                     |
|--------------|---------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| UC09-CT01    | Cadastrar ambiente (sucesso)                 | 1. Fazer login como Admin.<br>2. Preencher o formulário `"Cadastrar Novo Ambiente"` com dados válidos.<br>3. Submeter.                                                                                | `POST /api/environments` (com Token)<br>Body: `{"Name": "Titã", "Type": "Planetario", ...}`                                  | Status HTTP `201`.<br>JSON de resposta: objeto do novo ambiente criado.<br>A UI exibe mensagem de sucesso.                                      |
| UC09-CT02    | Tentar cadastrar (sem login)                 | 1. Tentar enviar a requisição de cadastro sem um Token de autenticação.                                                                                                                               | `POST /api/environments` (sem Token)<br>Body: `{"Name": "Titã", ...}`                                                        | Status HTTP `401` (Unauthorized).<br>JSON de resposta: `{"error": "Token de autenticação ausente."}`.                                           |
| UC09-CT03    | Tentar cadastrar (dados inválidos)           | 1. Fazer login como Admin.<br>2. Submeter o formulário de ambiente **sem** o campo obrigatório `Name`.                                                                                                | `POST /api/environments` (com Token)<br>Body: `{"Type": "Planetario", ...}`                                                  | Status HTTP `400` (Bad Request).<br>JSON de resposta: `{"error": "Os campos 'Name' e 'Type' são obrigatórios."}`.                               |

---

## 4. Critérios de Aceite Gerais

- O endpoint deve retornar o código HTTP especificado em cada teste.
- Quando aplicável, a UI deve refletir o comportamento esperado (redirecionamento, mensagem de erro, renderização correta).
- Operações que exigem autenticação **não devem** ser executadas sem Token válido.
- Entradas inválidas **devem** gerar mensagens de erro claras e status HTTP na faixa 4xx.
- Consultas com filtro (`q=`) não podem causar erro mesmo quando não há resultados; devem retornar lista vazia.

---

## 5. Ambiente de Teste

- Backend Node/Express (ou equivalente definido no TP4) ativo.
- Base de dados acessível (exceto nos testes que simulam falha de DB).
- Base de dados pré-populada com:
  - Pelo menos 2 culturas (ex: Mandioca, Batata-doce).
  - Pelo menos 2 ambientes (ex: Marte, ISS).
- Conta administrativa existente (`admin` / `admin`).
- Frontend carregável localmente para interações de UI (UC04, UC07, UC08, UC09).

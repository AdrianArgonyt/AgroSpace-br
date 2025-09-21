# Requisitos do Projeto — AgroSpace BR

## 1. Visão Geral
**Objetivo (ODS 9.5):** construir um guia simples que concentre informações e **simule viabilidade de cultivo** (“Planta × Ambiente”) em contextos educativos (Terra, ambientes análogos e planetários) e reúna conteúdos de **cultura científica/astronomia**.  
**Produto:** aplicação web com **frontend (HTML+JS)**, **backend (Flask/Python)** e **banco de dados (SQL Server Express 10GB)**.

## 2. Escopo do MVP (TP2)
- API funcionando para: **/health**, **/crops (GET/POST)**, **/environments (GET/POST)**, **/match (POST)**.  
- Tabelas **Crops** e **Environments** com **dados de exemplo** (seeds).  
- Página **HTML** que **lista** plantas e ambientes e roda o **simulador Planta × Ambiente**.  
- Página **“Sobre os dados”** com metodologia e aviso educacional.

> Fora do MVP (planejado para sprints seguintes): catálogo “Filmes & Ideias”, dashboard com métricas, mapa de atores, autenticação.

## 3. Atores / Perfis
- **Visitante/Estudante**: consulta catálogo, executa simulador.  
- **Conteudista/Admin**: cadastra plantas/ambientes e publica ajustes.

## 4. Requisitos Funcionais (RF)
**RF01. Healthcheck**  
Disponibilizar `GET /health` retornando `{ "status": "ok" }` para ver se a API está no ar.

**RF02. Listar plantas (GET /crops)**  
Retornar lista em JSON com: `Id, CommonName, ScientificName, Category, TempMinC, TempMaxC, PhMin, PhMax, PhotoperiodMinH, PhotoperiodMaxH, WaterNeed, EvidenceLevel`.

**RF03. Cadastrar planta (POST /crops)**  
Receber JSON com campos obrigatórios: `CommonName, Category, TempMinC, TempMaxC, PhMin, PhMax, WaterNeed, EvidenceLevel`. Responder com `id` criado.

**RF04. Listar ambientes (GET /environments)**  
Retornar `Id, Name, Type (Terra/Analogico/Planetario), TempMinC, TempMaxC, PressureKPa, GravityG, RadiationIndex, SoilPh, SoilType, WaterAvailability, PhotoperiodH, Atmosphere, EvidenceLevel`.

**RF05. Cadastrar ambiente (POST /environments)**  
Receber JSON com `Name, Type, TempMinC, TempMaxC, EvidenceLevel` e opcionais. Responder com `id` criado.

**RF06. Simulador Planta × Ambiente (POST /match)**  
Entrada: `{ "crop_id": <int>, "env_id": <int>, "infra": ["estufa","luz_artificial","hidroponia"] }`.  
Saída: `{ "crop": ..., "environment": ..., "score": 0..100, "limiting_factors": [], "rationale": [] }`.

**RF07. Página HTML base**  
Disponibilizar `index.html` com abas: **Cultura & Cinema**, **Agro Planetário (tabelas + simulador)**, **Dashboard (placeholder)**, **Sobre os Dados**.

**RF08. Integração Front–API**  
Arquivo `web/app.js` com funções `apiGet`/`apiPost` (fetch) e scripts para:
- Popular tabelas de **Plantas** e **Ambientes**.
- Executar o **/match** e renderizar score, fatores e justificativas.

**RF09. “Sobre os Dados” (metodologia + aviso)**  
Página descrevendo que os resultados são **educacionais**, que ambientes não-terrestres **exigem infraestrutura** (pressurização, iluminação, proteção) e níveis de evidência: **validado/experimental/exploratório**.

**RF10. Erros padronizados**  
Retornar erros em JSON: `{ "error": "<mensagem>" }` para entradas inválidas, 404 e 500.

> **Evoluções planejadas**  
RF11. Catálogo “Filmes & Ideias” (listar/recomendar).  
RF12. Dashboard simples (contadores por tipos/tempo).

## 5. Requisitos Não Funcionais (RNF)
**RNF01. Arquitetura:** Frontend HTML/JS estático; Backend Flask (Python 3.11+); Banco SQL Server Express.  
**RNF02. Desempenho:** `GET` principais respondem em **P95 < 500 ms** em ambiente local com seed.  
**RNF03. Acessibilidade/Usabilidade:** HTML responsivo e sem bloqueios de CORS (habilitar `flask-cors`).  
**RNF04. Segurança/Privacidade:** sem dados pessoais; `.env` fora do versionamento; TLS quando publicado.  
**RNF05. Qualidade de Código:** mensagens de erro claras; logs básicos de erro no backend.  
**RNF06. Transparência:** toda tela que exiba o score traz o **rationale** (explicações) e o **nível de evidência** dos dados.  
**RNF07. Deploy Dev:** execução local documentada no `README.md` (passo a passo).  
**RNF08. Manutenibilidade:** camadas separadas (`api/routers`, `api/models`, `web/`), scripts SQL (`schema.sql`, `seed.sql`).

## 6. Regras de Negócio (RB)
**RB01. Evidência:** cada planta/ambiente possui `EvidenceLevel` ∈ {`validado`, `experimental`, `exploratorio`}.  
**RB02. Score de compatibilidade:** média ponderada (exemplo de MVP): Temp 30%, pH 20%, Fotoperíodo 20%, Água 15%, Ambiente-base 15%, com **penalidades** quando `Type != Terra` e **infraestrutura** não marcada.  
**RB03. Justificativas:** toda resposta do simulador deve incluir **3–5 justificativas** claras (temperatura, pH, água, fotoperíodo, infraestrutura).  
**RB04. Avisos educativos:** para ambientes não-terrestres, **sempre** exibir nota “requer estufa/pressurização/iluminação/ proteção” conforme o caso.

## 7. Dados & Modelo (resumo inicial)
**Crops**  
- `Id (PK)`, `CommonName`, `ScientificName?`, `Category`,  
- `TempMinC`, `TempMaxC`, `PhMin`, `PhMax`,  
- `PhotoperiodMinH?`, `PhotoperiodMaxH?`,  
- `WaterNeed (baixa|media|alta)`, `EvidenceLevel`, `Sources?`.

**Environments**  
- `Id (PK)`, `Name`, `Type (Terra|Analogico|Planetario)`,  
- `TempMinC`, `TempMaxC`, `PressureKPa?`, `GravityG?`, `RadiationIndex?`,  
- `SoilPh?`, `SoilType?`, `WaterAvailability? (baixa|media|alta)`,  
- `PhotoperiodH?`, `Atmosphere?`, `EvidenceLevel`, `Notes?`, `Sources?`.

> Seeds mínimos: Alface, Tomate; Terra-Argissolo, Marte-Externo.

## 8. Endpoints (MVP)
- `GET /health` → `{ "status": "ok" }`  
- `GET /crops` → lista de plantas (filtros simples por `?category=` em evolução)  
- `POST /crops` → cria planta  
- `GET /environments` → lista ambientes  
- `POST /environments` → cria ambiente  
- `POST /match` → `{ score, limiting_factors[], rationale[] }`

## 9. Critérios de Aceitação (principais)
**CA-RF02 (GET /crops):**  
- Dado DB com seeds, quando acessar `/crops`, então retorna **200** com **>= 2 itens** e campos conforme modelo.

**CA-RF03 (POST /crops):**  
- Dado JSON válido, quando enviar para `/crops`, então retorna **201** com `id`; um novo `GET /crops` contém o item.

**CA-RF06 (POST /match):**  
- Dado `crop_id` e `env_id` válidos, quando enviar para `/match`, então retorna **200** com `score ∈ [0,100]`, **>= 2** itens em `limiting_factors` se houver problemas, e **>= 3** frases em `rationale`.

**CA-RF08 (Front–API):**  
- Dado `index.html` aberto, quando clicar para “calcular”, então exibe o **score** e justificativas sem recarregar a página.

**CA-RF10 (Erros):**  
- Dado um pedido inválido, quando enviar para qualquer endpoint, então retorna **4xx** com JSON `{ "error": "mensagem" }`.

## 10. Restrições & Riscos
- **Sem dados pessoais**; foco educativo.  
- **Dependência de ambiente local** (SQL/ODBC) — mitigar com README e `.env.example`.  
- Possível **imprecisão científica** — mitigar com **nível de evidência** e “Sobre os dados”.

## 11. Métricas (KPI simples do MVP)
- Nº de plantas/ambientes cadastrados.  
- Nº de simulações executadas (contador simples no backend).  
- Tempo médio de resposta dos `GET`.

## 12. Evolução (Backlog futuro)
- Catálogo **Filmes & Ideias** (lista/recomendações).  
- **Dashboard** com contadores e séries (por mês).  
- **Mapa** de atores (parcerias) — apenas descritivo.  
- Autenticação **Admin** (CRUD seguro).



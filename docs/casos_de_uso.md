# Casos de Uso — AgroSpace BR

## Atores
- **Visitante/Estudante**: acessa o site, lista dados e roda o simulador.
- **Conteudista/Admin**: insere/atualiza plantas e ambientes (via endpoints POST).

## Lista de Casos (MVP)
1. **UC-01 — Verificar saúde da API**
   - Ator: Visitante
   - Objetivo: Checar se o servidor está no ar.
   - Fluxo principal: acessar `GET /health` → retorna `{"status":"ok"}`.

2. **UC-02 — Listar Plantas**
   - Ator: Visitante
   - Objetivo: Ver a lista de plantas (nome, categoria, faixas de temp/pH).
   - Fluxo principal: `GET /crops` → JSON com registros.

3. **UC-03 — Cadastrar Planta**
   - Ator: Admin
   - Objetivo: Inserir uma nova planta.
   - Fluxo principal: `POST /crops` com JSON válido → retorna `id`.
   - Regras: campos obrigatórios (CommonName, Category, TempMinC, TempMaxC, PhMin, PhMax, WaterNeed, EvidenceLevel).
   - Exceções: JSON inválido → 400 `{ "error": "..." }`.

4. **UC-04 — Listar Ambientes**
   - Ator: Visitante
   - Objetivo: Ver a lista de ambientes (Terra/Analógico/Planetário e parâmetros).
   - Fluxo principal: `GET /environments` → JSON.

5. **UC-05 — Cadastrar Ambiente**
   - Ator: Admin
   - Objetivo: Inserir um novo ambiente.
   - Fluxo principal: `POST /environments` com JSON válido → retorna `id`.
   - Regras: campos obrigatórios (Name, Type, TempMinC, TempMaxC, EvidenceLevel).
   - Exceções: JSON inválido → 400.

6. **UC-06 — Simular Planta × Ambiente**
   - Ator: Visitante
   - Objetivo: Comparar uma planta com um ambiente e obter um **score** (0–100) + **fatores limitantes** + **rationale**.
   - Fluxo principal: `POST /match` com `{ crop_id, env_id, infra[] }` → JSON com resultados.
   - Regras: penalidade quando `Type != Terra` sem “estufa/hidroponia”.
   - Exceções: ids inexistentes → 400; erro interno → 500.

7. **UC-07 — Ver “Sobre os Dados”**
   - Ator: Visitante
   - Objetivo: Ler metodologia, limites e níveis de evidência.
   - Fluxo principal: abrir a aba **Sobre os Dados** no HTML.

## Relações entre casos (texto)
- **UC-02** e **UC-04** alimentam os **selects** do **UC-06**.
- **UC-03** e **UC-05** estendem o cadastro, refletindo nos casos de listagem.
- **UC-06** depende de dados existentes (seeds ou cadastros).

## Critérios de Aceitação (exemplos)
- **CA UC-02**: “Dado banco com seeds, quando chamar `/crops`, então recebo 200 e uma lista com ≥2 itens contendo os campos do modelo.”
- **CA UC-06**: “Dado `crop_id=1` e `env_id=2`, quando chamar `/match`, então recebo 200 com `score ∈ [0,100]`, ao menos 1 fator limitante (se aplicável) e pelo menos 3 frases em `rationale`.”

## Regras de Negócio (essenciais)
- **RB-01**: `EvidenceLevel ∈ {validado, experimental, exploratorio}`.
- **RB-02**: `score` calculado pela média ponderada (Temp 30%, pH 20%, Fotoperíodo 20%, Água 15%, Ambiente 15%) com penalidades se `Type != Terra` e infra não marcada.
- **RB-03**: Exibir sempre nota educativa para ambientes não-terrestres (“requer estufa/pressurização/iluminação/proteção”).

## Observações de UI
- HTML com abas: **Agro Planetário** (tabelas + simulador) e **Sobre os Dados**.
- Em **Agro Planetário**, exibir tabelas com filtros simples e o painel de resultado do simulador (score, fatores e rationale).

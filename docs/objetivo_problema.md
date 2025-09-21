# Objetivo & Problema — AgroSpace BR

## 1) Contexto
O projeto faz parte da disciplina de Engenharia de Software. O produto é um **guia web** com:
- Catálogo simples de **plantas** (frutas/verduras) e **ambientes**.
- Um **simulador** que compara “Planta × Ambiente” e gera um **score de viabilidade** educativo.
- Uma aba “**Sobre os Dados**” explicando a metodologia e limites.
- (Evolução posterior) Conteúdos de **Cultura & Cinema** (astronomia) e **dashboard**.

Alinhamento com **ODS 9 (meta 9.5)**: fortalecer capacidades tecnológicas/educacionais criando infraestrutura de informação e simulações didáticas.

## 2) Problema
As informações sobre cultivo (faixa de temperatura, pH, água) e sobre ambientes (Terra, análogos, cenários planetários) estão **espalhadas**. Para uso **educacional**, faz falta um lugar simples que:
- centralize **plantas** e **ambientes**,
- permita **simular** compatibilidade com explicações,
- deixe claro o **nível de evidência** (validado / experimental / exploratório).

## 3) Objetivo do Produto
Entregar um **MVP funcional** que:
- disponibilize uma **API** (Flask + SQL Server) com endpoints para plantas, ambientes e simulador;
- tenha uma **página HTML** simples que consome a API (listar dados + rodar o simulador);
- documente a **metodologia** (educativa, não prescritiva).

## 4) Escopo (MVP / esta etapa)
**Dentro**:
- `GET/POST /crops`, `GET/POST /environments`, `POST /match`, `GET /health`.
- Seeds (2–3 plantas e 2 ambientes).
- HTML + JS consumindo a API (listar + simular).
- Página “Sobre os dados”.

**Fora (próximas sprints)**:
- Catálogo **Filmes & Ideias** (astronomia).
- **Dashboard** com métricas.
- Autenticação/Admin.
- Mapa de atores.

## 5) Público-alvo (personas rápidas)
- **Estudante/Visitante**: quer aprender e brincar com o simulador.
- **Conteudista/Admin**: cadastra plantas e ambientes (dados de exemplo).

## 6) Benefícios esperados
- **Aprendizado**: entender, com linguagem simples, por que um cultivo seria viável/inviável em certos contextos.
- **Organização**: centralizar dados mínimos (plantas/ambientes) para demonstrações em aula.
- **Transparência**: cada simulação traz justificativas (“rationale”) e níveis de evidência.

## 7) Sucesso (critérios)
- API responde aos endpoints do MVP.
- HTML lista dados e executa o simulador sem erros.
- README permite que outra pessoa suba o projeto localmente.
- Project (kanban) com planejamento do TP2 preenchido.

## 8) Riscos e mitigação
- **Dados imprecisos** → marcar **nível de evidência** e avisos claros (educacional).
- **Ambiente local** (ODBC/SQL) → README detalhado + `.env.example`.
- **Tempo curto** → focar MVP (listar + simular); deixar extras para sprint seguinte.

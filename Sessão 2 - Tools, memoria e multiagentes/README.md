# Sessão 2 - Tools, Memory & Multiagents

Nesta aula avançamos da construção básica de agentes para tools fundamentais em aplicações reais:

- RAG (Retrieval Augmented Generation)
- NL2SQL (Natural Language to SQL)
- MCP (Model Context Protocol)

O objetivo aqui não é apenas rodar código, mas entender como estruturar tipos diferentes de acesso a conhecimento:

- Dados não estruturados (documentos, textos, base interna)
- Dados estruturados (banco relacional)
- Protocolo de comunicação

A organização do repositório reflete exatamente essa separação.

---

# Estrutura dos Arquivos
```
.
├── .env
├── 2.1 - Banco vetorial.ipynb
├── 2.2 - NL2SQL.ipynb
├── 2.3 - Agent MCP.json
├── 2.3 - MCP server.json
├── 2.4 - Agent MCP.json
├── 2.4 - MCP server (RAG + NL2SQL).json
├── 2.4.1 - Agent MCP - Suporte direto.json
├── 2.5 - Agent MCP.json
├── 2.5 - MCP server (RAG + NL2SQL + HTTPS).json
├── manual.txt
└── README.md
```
Cada arquivo representa um bloco independente da arquitetura.
Todos os aruqivos `.json` são fluxos do n8n que podem ser importados para reprodução de todos os materiais apresentados em aula.

---

# 2.1 – Banco Vetorial

Neste notebook implementamos um pipeline completo de RAG.

Aqui trabalhamos com:

- Ingestão de texto
- Geração de embeddings
- Quebra em chunks
- Armazenamento vetorial
- Busca por similaridade
- Uso do contexto recuperado como janela da LLM

A ideia central é permitir que o modelo consulte uma base de conhecimento sem precisar ter tudo no prompt.

Esse padrão é o que viabiliza agentes que trabalham com:

- Manuais internos
- Documentações técnicas
- Base de tickets
- Conteúdo institucional
- Dados não estruturados em geral

Resolve o problema de memória externa do modelo.

---

# 2.2 – NL2SQL

Neste notebook implementamos a conversão de linguagem natural em consultas SQL executáveis.

Aqui trabalhamos com:

- Estrutura do schema do banco
- Construção de prompt restritivo
- Geração automática de query
- Validação da consulta
- Execução no banco
- Retorno estruturado de resultados

Esse padrão permite que o agente interaja diretamente com dados estruturados.

É o que viabiliza perguntas como:

- “Quantos tickets estão abertos?”
- “Qual empresa tem mais incidentes P1?”
- “Qual o total de chamados no último mês?”

Sem que o usuário precise saber o que é um comando SQL.

---

# MCP – Exposição dos Agentes como Serviço

Após a construção dos pipelines de RAG e NL2SQL, esta etapa apresenta a evolução da arquitetura: expor os agentes como serviços externos utilizando MCP (Model Context Protocol).

A evolução ocorre em etapas:

### 2.3 – Estrutura básica de MCP

- Criação do agente no n8n
- Configuração inicial do servidor MCP
- Conexão entre agente e servidor

Aqui o foco é entender a estrutura mínima necessária para expor uma tool via MCP.

---

### 2.4 – Integração RAG + NL2SQL

- Consolidação das ferramentas construídas anteriormente
- Exposição de múltiplas capacidades em um único servidor
- Decisão dinâmica entre consulta vetorial e consulta SQL

Neste ponto, o agente já é capaz de operar com duas fontes distintas de conhecimento.

---

### 2.4.1 – Suporte Direto

Versão extra do agente com a mesma base de conhecimento, consultando o mesmo servidor, mas agora atendendo como assistente de suporte.

Útil para entender:

- Vantagens de servidor MCP com replicação de tools
- Aplicação muito aproveitada no mundo corporativo em uma versão prática e simples


---

### 2.5 – Servidor com HTTPS

Nesta etapa final:

- Um endpoint é exposto em uma VM e adicionado como ferramenta do MCP
- Agora todos os três tipos de tools mais utilizados no mercado fazem parte de um único agente
- Integração com infraestrutura externa

Aqui o objetivo é mostrar como sair do ambiente puramente local e estruturar algo mais realista do ponto de vista arquitetural.

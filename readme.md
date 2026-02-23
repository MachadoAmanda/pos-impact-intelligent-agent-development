# Intelligent Agent Development: do Protótipo à Produção

Repositório oficial da disciplina ministrada por Amanda Machado.

Aqui estão os códigos, exemplos e práticas desenvolvidas ao longo da disciplina.
A proposta é simples: ensinar você a construir agentes que funcionam no mundo real.


## Como a disciplina está organizada

O conteúdo está dividido em 3 sessões e o repositório segue exatamente essa estrutura:
```
.
├── Sessão 1 - fundamentos de agentes/
├── Sessão 2 - tools memoria multiagentes/
├── Sessão 3 - producao e escala/
└── README.md
```
## 1. Fundamentos de Agentes

Antes de usar tools, frameworks ou qualquer coisa sofisticada, precisamos entender:

- O que é (de verdade) um agente
- Quando faz sentido usar
- Diferença entre agente e workflow tradicional
- Loop de decisão
- Níveis de autonomia

Você vai construir um agente simples e entender a arquitetura mínima necessária.

Objetivo: sair do modismo e ganhar clareza arquitetural.

## 2. Tools, Memória e Multiagentes

Aqui os agentes deixam de ser "brinquedo" e começam a ganhar capacidades reais:

- Integração com APIs
- RAG
- NL2SQL
- Memória
- Sistemas multiagentes

Objetivo: fazer o agente agir no mundo externo.

## 3. Produção e Escala

A maioria dos projetos para aqui, mas produto de verdade começa aqui.

Vamos falar sobre:

- Arquitetura de produção
- Avaliação
- Observabilidade
- Confiabilidade
- Segurança
- Custo
- Guardrails

Objetivo: transformar protótipos em sistemas previsíveis e sustentáveis.

## Como usar este repositório
### Siga a ordem das pastas

O conteúdo foi pensado de forma progressiva.
Evite pular direto para produção sem entender fundamentos.

### Configure a LLM

Como já visto em classe, os agentes são dependentes das LLMs, para isso você precisa configurar a sua, você pode usar qualquer uma, mas eu recomendo que seja OpenAI compatible para que você não tenha que adaptar tanto o código. 

**Complementar:** Uma dica para não ter nenhum custo com LLMs é fazer uma conta trial na OCI (https://signup.oraclecloud.com/), você vai ganhar 300USD de crédito para usar com qualquer modelo disponível. Lembrando que isso é opcional, você também pode optar por fazer uma conta na OpenAI que vai funcionar igual. 

O importante é configurar o arquivo `.env` com as suas credenciais. 

### Rode os exemplos

Cada pasta contém códigos executáveis.

Passos básicos:
``` python
git clone <repo>
cd <repo>
python -m venv .venv
.venv\Scripts\activate  # Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Depois, execute os exemplos de cada módulo.

### Modifique os exemplos

Não apenas rode o código.
Quebre. Mude. Teste limites.

O aprendizado real vem da experimentação.


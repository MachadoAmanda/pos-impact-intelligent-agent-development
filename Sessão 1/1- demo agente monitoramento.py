import streamlit as st
import random
import json
import time
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# =========================
# CONFIG
# =========================
base_url = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1"
api_key = os.getenv("OCI_API_KEY")

st.set_page_config(layout="wide")

client =  OpenAI(
        base_url=base_url,
        api_key=api_key
    )

REGIONS = ["Norte","Sul","Leste","Oeste"]

# =========================
# MOCK TOOLS
# =========================

def check_sensor(region):
    return {
        "region": region,
        "pressure": random.randint(30,100),
        "flow": random.randint(10,90),
        "health": random.choice(["ok","suspect"])
    }

def check_machine(region):
    return random.choice([
        "normal",
        "vibration",
        "overheating"
    ])

def lookup_docs(topic):
    return f"Procedimento padrão para {topic}: inspeção técnica e registro."

def notify(team, message):
    return f"Notificado {team} com mensagem: {message}"

TOOLS = {
    "check_sensor": check_sensor,
    "check_machine": check_machine,
    "lookup_docs": lookup_docs,
    "notify": notify
}

# =========================
# UI CARD
# =========================

def render_card(text, color="#1f77b4"):

    st.markdown(f"""
    <div style="
        padding:16px;
        border-radius:10px;
        margin:8px 0;
        background:{color}22;
        border-left:6px solid {color};
    ">
    {text}
    </div>
    """, unsafe_allow_html=True)

# =========================
# LLM CALL
# =========================

def ask_llm(system, user):

    resp = client.chat.completions.create(
        model="xai.grok-4-fast-non-reasoning",
        messages=[
            {"role":"system","content":system},
            {"role":"user","content":user}
        ],
        temperature=0.2
    )

    return resp.choices[0].message.content

# =========================
# AGENTE
# =========================

def run_agent():

    goal = "Avaliar saúde da infraestrutura de saneamento"

    state = {
        "checked_regions": [],
        "findings": []
    }

    for step in range(6):

        decision_prompt = f"""
Objetivo: {goal}

Estado atual:
{json.dumps(state,indent=2)}

Regiões disponíveis:
{REGIONS}

Decida a próxima ação.

Responda SOMENTE JSON:

{{
  "action": "...",
  "reason": "...",
  "input": {{}}
}}

Ações possíveis:
- check_sensor
- check_machine
- lookup_docs
- notify
- finish

Se já houver dados suficientes, escolha finish.
"""

        decision = ask_llm(
            "Você é um agente autônomo operacional. Suas operações tem base nas informações e missão que você recebeu. Sempre use Portugues como lingua principal.",
            decision_prompt
        )

        decision = json.loads(decision)

        render_card(
            f"Decisão: {decision['action']}<br>Motivo: {decision['reason']}",
            "#6a1b9a"
        )

        if decision["action"] == "finish":
            break

        tool = TOOLS[decision["action"]]

        result = tool(**decision["input"])

        render_card(
            f"Tool executada: {decision['action']}<br>Resultado: {result}",
            "#ff9800"
        )

        # atualizar estado
        state["findings"].append({
            "action":decision["action"],
            "input":decision["input"],
            "result":result
        })

        if "region" in decision["input"]:
            state["checked_regions"].append(
                decision["input"]["region"]
            )

        time.sleep(1)

    # =====================
    # RELATÓRIO FINAL
    # =====================

    email_prompt = f"""
Com base nos dados:

{json.dumps(state,indent=2)}

Escreva um email operacional contendo:

- regiões analisadas
- problemas encontrados
- quem foi notificado
- recomendações
"""

    email = ask_llm(
        "Você é um especialista em operações de saneamento.",
        email_prompt
    )

    render_card(email, "#2e7d32")

# =========================
# TIMER
# =========================

if "next_run" not in st.session_state:
    st.session_state.next_run = datetime.now() + timedelta(
        minutes=random.randint(1,120)
    )

remaining = int(
    (st.session_state.next_run - datetime.now()).total_seconds()/60
)

st.info(f"Próxima execução automática estimada em {remaining} minutos")

# =========================
# UI
# =========================

st.title("Agente Autônomo de Monitoramento")

if st.button("Disparar verificação agora"):

    run_agent()

    st.session_state.next_run = datetime.now() + timedelta(
        minutes=random.randint(1,120)
    )

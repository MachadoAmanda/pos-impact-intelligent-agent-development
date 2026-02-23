# ==========================================
#   README
#
#   Antes de rodar o código instale: 
#   pip install streamlit langchain langchain-oci requests
#
#   Para rodar a interface:
#   streamlit run <file-name>.py
#
# ===========================================


import streamlit as st
import requests
import json

from langchain_core.tools import tool
from langchain_core.callbacks import BaseCallbackHandler
from langchain.agents import create_agent
from langchain_core.messages import AIMessage



# =========================
# WEATHER TOOL
# =========================
@tool
def get_weather(latitude: str, longitude: str) -> str:
    """Obtém o clima atual usando latitude e longitude."""

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m,wind_speed_10m"
    )

    response = requests.get(url)
    return str(response.json())


# =========================
# CALLBACK
# =========================
class CleanAgentCallback(BaseCallbackHandler):

    def on_tool_start(self, serialized, input_str, **kwargs):
        print(f"\n TOOL: {serialized.get('name')}")
        print(f"↳ input: {input_str}")

    def on_tool_end(self, output, **kwargs):
        print("\n TOOL RESULT:")

        content = getattr(output, "content", output)

        try:
            data = json.loads(content)
            if "current" in data:
                print("Temperatura:", data["current"]["temperature_2m"])
                print("Vento:", data["current"]["wind_speed_10m"])
        except:
            print(content[:200])


# =========================
# LLM OCI
# =========================
from dotenv import load_dotenv
import os

load_dotenv()

base_url = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1"  # ou sua URL
api_key = os.getenv("OCI_API_KEY")

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="xai.grok-4-fast-non-reasoning",
    temperature=0.2,
    max_tokens=500,
    streaming=False,
    api_key=api_key,
    base_url=base_url
)
tools = [get_weather]


# =========================
# PROMPT
# =========================
react_prompt_template = """You are a helpful weather assistant.

You can choose latitude and longitude yourself.

IMPORTANT:
- Always choose coordinates
- Analyze tool results
- Never output raw JSON
- DO NOT use tools, when the question can be answered without real-time data. 
- Answer in the same language as the user question

{tools}

Begin!
"""

agent = create_agent(
    llm,
    tools,
    system_prompt=react_prompt_template
)


# =========================
# EXTRAIR RESPOSTA
# =========================
def extract_final_output(agent_response):
    for msg in reversed(agent_response["messages"]):
        if isinstance(msg, AIMessage) and msg.content:
            if "Final Answer:" in msg.content:
                return msg.content.split("Final Answer:",1)[1].strip()
            return msg.content.strip()


# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="Weather Chatbot", page_icon="🌤️")

st.title("🌤️ Weather Chatbot")
st.write("Pergunte sobre o clima de qualquer lugar do mundo!")

if "messages" not in st.session_state:
    st.session_state.messages = []


# Mostrar histórico
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Input do usuário
if prompt := st.chat_input("Pergunte sobre o clima..."):

    st.session_state.messages.append({"role":"user","content":prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    callback = CleanAgentCallback()

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = agent.invoke(
                {"messages": prompt},
                config={"callbacks":[callback]}
            )

            final_answer = extract_final_output(response)

            st.markdown(final_answer)

    st.session_state.messages.append(
        {"role":"assistant","content":final_answer}
    )

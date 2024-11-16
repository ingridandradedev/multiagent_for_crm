import streamlit as st
import requests
import json

# Título e descrição
st.title("💬 Chatbot com LangFlow API")
st.write(
    "Este chatbot utiliza a API do LangFlow para gerar respostas. "
    "Digite uma mensagem e veja como ele responde!"
)

# Configurações da API
BASE_API_URL = "https://langflowailangflowlatest-production-74ad.up.railway.app"
FLOW_ID = "a7fb02e1-7f56-48a3-adb7-d7cc414e3247"
ENDPOINT = FLOW_ID  # Utilize o endpoint ou ID do fluxo
HEADERS = {"Content-Type": "application/json"}
TWEAKS = {}  # Ajuste os componentes aqui, se necessário.

# Função para chamar a API do LangFlow
def call_langflow_api(message, endpoint=ENDPOINT, tweaks=None):
    url = f"{BASE_API_URL}/api/v1/run/{endpoint}"
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    if tweaks:
        payload["tweaks"] = tweaks

    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao conectar-se à API do LangFlow: {e}")
        return None

# Manter mensagens no estado da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir mensagens do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada para o usuário
if prompt := st.chat_input("Digite sua mensagem:"):
    # Adicionar mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Enviar mensagem para a API
    response_data = call_langflow_api(prompt, tweaks=TWEAKS)

    if response_data:
        try:
            # Extrair a resposta da API
            ai_message = response_data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            # Adicionar a resposta ao histórico
            st.session_state.messages.append({"role": "assistant", "content": ai_message})
            with st.chat_message("assistant"):
                st.markdown(ai_message)
        except KeyError:
            st.error("Erro ao processar a resposta da API.")

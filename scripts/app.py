import streamlit as st
import requests
import uuid
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="BimBam Buy - Suporte de Pagamentos",
    page_icon="🛍️",
    layout="centered"
)

# Configurações do n8n
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "COLOQUE_A_URL_DO_WEBHOOK_AQUI")

# Cabeçalho da interface
st.title("🛍️ BimBam Buy - Assistente Virtual")
st.caption("Tire suas dúvidas sobre métodos de pagamento, reembolsos e prazos em tempo real.")

# Inicializa variáveis de sessão
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou o assistente virtual da BimBam Buy. Como posso te ajudar com seu pagamento hoje?"}
    ]

# Exibe mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de texto do usuário
if prompt := st.chat_input("Digite sua dúvida aqui..."):
    # Mostra a mensagem do usuário na tela
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Chamada para o backend (n8n)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        if N8N_WEBHOOK_URL == "COLOQUE_A_URL_DO_WEBHOOK_AQUI" or not N8N_WEBHOOK_URL:
            st.error("⚠️ URL do Webhook do n8n não configurada. Renomeie o arquivo `.env.example` para `.env` e coloque sua URL real lá.")
        else:
            with st.spinner("Consultando base de conhecimento da BimBam Buy..."):
                # Enviamos o sessionId para manter a memória separada por usuário no n8n
                payload = {
                    "sessionId": st.session_state.session_id,
                    "chatInput": prompt
                }
                
                try:
                    # Envia requisição POST para o Webhook do n8n
                    response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=30)
                    response.raise_for_status() # Verifica se ocorreu erro HTTP (4xx, 5xx)
                    
                    data = response.json()
                    # A chave de resposta 'output' depende do formato de saída do Agent no n8n.
                    # Se o Agent retornar apenas texto, pode ser que precise ajustar a chave abaixo.
                    resposta_texto = data.get("output", "Desculpe, a resposta do agente veio em um formato inesperado.")
                    
                    message_placeholder.markdown(resposta_texto)
                    st.session_state.messages.append({"role": "assistant", "content": resposta_texto})
                    
                except requests.exceptions.Timeout:
                    st.error("Tempo de resposta esgotado. O n8n demorou muito para responder.")
                except requests.exceptions.ConnectionError:
                    st.error("Falha ao conectar no n8n. Verifique se o fluxo está ativo ou se a URL está correta.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Erro ao processar a requisição: {e}")
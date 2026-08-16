import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="BimBam Buy - Suporte de Pagamentos",
    page_icon="🛍️",
    layout="centered"
)

# Cabeçalho da interface
st.title("🛍️ BimBam Buy - Assistente Virtual")
st.caption("Tire suas dúvidas sobre métodos de pagamento, reembolsos e prazos em tempo real.")

# Inicializa o histórico do chat
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

    # Resposta simulada (Aqui você conecta a Webhook API do seu n8n)
    with st.chat_message("assistant"):
        response = f"Recebi sua pergunta: '{prompt}'. Estou consultando o documento oficial da BimBam Buy..."
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
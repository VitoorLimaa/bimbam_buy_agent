# BimBam Buy - Assistente Virtual (RAG Agent) 🛍️🤖

Este projeto consiste em um Assistente Virtual de suporte focado em dúvidas sobre métodos de pagamento, reembolsos e prazos da loja fictícia **BimBam Buy**. Ele foi construído utilizando uma arquitetura de Geração Aumentada por Recuperação (RAG) através de fluxos automatizados no **n8n** e uma interface de usuário no **Streamlit**.

---



## 📂 Estrutura de Arquivos

```text
bimbam-buy-agent/
│
├── README.md                           # Documentação do projeto
├── Workflow_n8n/
│   └── Agente_n8n_final.json           # Fluxo exportado do n8n (Agent RAG + Ingestão)
└── scripts/
    └── app.py                          # Interface do Chatbot em Streamlit
```

---

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de ter os seguintes itens:
- **Python 3.8+** instalado em sua máquina.
- Conta e acesso a uma instância do **n8n** (Cloud ou Self-hosted).
- Chave de API da **OpenAI**.
- Conta e Index configurado no banco vetorial **Pinecone**.
- Pasta no **Google Drive** para armazenar os documentos (PDFs) da loja.

---

## 🚀 Como Configurar e Executar

### 1. Configurando o Backend (n8n)
1. Abra sua instância do [n8n](https://n8n.io/).
2. Vá em **Workflows** e selecione **Import from File**.
3. Importe o arquivo `Agente_n8n_final.json` que está na pasta `Workflow_n8n/`.
4. **Configure as Credenciais:**
   - **Google Drive:** Conecte sua conta e insira o ID da pasta onde os PDFs base de conhecimento serão salvos.
   - **Pinecone Vector Store:** Insira suas credenciais (API Key, Environment e Nome do Index).
   - **OpenAI:** Cadastre sua chave da OpenAI nos nós de *Embeddings* e no nó do *Chat Model*.
5. Salve e **Ative o Workflow** no canto superior direito para que o Webhook e o Gatilho do Drive fiquem online.

### 2. Configurando o Frontend (Streamlit)
Instale as bibliotecas necessárias para rodar o app localmente:
```bash
pip install streamlit requests
```

Para conectar a interface visual ao agente, edite o arquivo `scripts/app.py`, integrando o chat com o Webhook do n8n:
```python
# Exemplo de integração no app.py usando a biblioteca 'requests'
import requests
import streamlit as st

# ... código de setup do streamlit ...

if prompt := st.chat_input("Digite sua dúvida aqui..."):
    # Exibe mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Chama o n8n e exibe a resposta
    with st.chat_message("assistant"):
        # Substitua pela Test URL ou Production URL do seu nó Webhook no n8n
        url_n8n = "URL_DO_SEU_WEBHOOK_N8N_AQUI"
        
        payload = {"message": prompt}
        try:
            # Faz a requisição POST para o n8n
            resposta_api = requests.post(url_n8n, json=payload).json()
            
            # Ajuste a chave de resposta de acordo com o retorno do AI Agent do n8n (ex: ['output'])
            resposta_texto = resposta_api.get('output', 'Desculpe, não consegui entender.') 
        except Exception as e:
            resposta_texto = "Erro ao conectar com o Agente n8n."
            
        st.markdown(resposta_texto)
        st.session_state.messages.append({"role": "assistant", "content": resposta_texto})
```

Para rodar a interface web, abra seu terminal na raiz do projeto e execute:
```bash
streamlit run scripts/app.py
```

---

## 🛠️ Tecnologias Utilizadas
- **n8n:** Automação e Orquestração do RAG (Advanced AI Nodes)
- **Streamlit:** Interface web (Python)
- **OpenAI (GPT-4o):** Inteligência Artificial e Embeddings
- **Pinecone:** Banco de Dados Vetorial para busca semântica
- **Google Drive:** Repositório de arquivos para ingestão de conhecimento

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Task Notifier", page_icon="🎯", layout="centered")

st.markdown("""
    <style>
        /* Título em Degradê Moderno */
        .main-title {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(45deg, #4F8BF9, #29B6F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0px;
        }
        .subtitle {
            color: #6A7B95;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        
        /* Cards das Tarefas */
        .task-card-pending {
            background: rgba(79, 139, 249, 0.08);
            border-left: 5px solid #4F8BF9;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            font-size: 1.1rem;
        }
        .task-card-completed {
            background: rgba(46, 204, 113, 0.08);
            border-left: 5px solid #2ecc71;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
            font-size: 1.1rem;
            text-decoration: line-through;
            color: #7f8c8d;
        }
        
        /* Ajuste fino para os botões ficarem alinhados verticalmente */
        .stButton > button {
            margin-top: 8px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🎯 Task Notifier</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Gerencie suas tarefas com notificações automáticas via Telegram</p>', unsafe_allow_html=True)

with st.container():
    st.markdown("### ➕ Nova Tarefa")
    col_input, col_id = st.columns([2, 1])
    
    with col_input:
        titulo = st.text_input("O que precisa ser feito?", placeholder="Ex: Estudar FastAPI e Streamlit")
    with col_id:
        destinatario = st.text_input("Chat ID do Telegram:", value="7224724165")
        
    if st.button("🚀 Criar e Notificar", use_container_width=True):
        if titulo:
            with st.spinner("Enviando notificação..."):
                resp = requests.post(f"{API_URL}/tasks/", params={"titulo": titulo, "destinatario": destinatario})
                if resp.status_code == 200:
                    st.toast("Tarefa criada com sucesso! 🎉", icon="✅")
                    st.rerun()
        else:
            st.error("Por favor, digite um título para a tarefa!")

st.markdown("---")

st.markdown("### 📋 Minhas Tarefas")

try:
    tarefas = requests.get(f"{API_URL}/tasks/").json()
except Exception:
    st.error("Erro ao conectar com a API. Certifique-se de que o backend está rodando!")
    tarefas = []

if not tarefas:
    st.info("💡 Nenhuma tarefa por aqui ainda. Adicione uma acima!")
else:
    for t in tarefas:
        col_text, col_action, col_delete = st.columns([5, 2, 1])
        
        with col_text:
            if t["concluida"]:
                st.markdown(f'<div class="task-card-completed">🎉 {t["titulo"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="task-card-pending">⏳ {t["titulo"]}</div>', unsafe_allow_html=True)
        
        with col_action:
            if not t["concluida"]:
                if st.button("Concluir", key=f"ok_{t['id']}", use_container_width=True, type="primary"):
                    requests.put(f"{API_URL}/tasks/{t['id']}", params={"concluida": True})
                    st.rerun()
            else:
                if st.button("Reabrir", key=f"re_{t['id']}", use_container_width=True):
                    requests.put(f"{API_URL}/tasks/{t['id']}", params={"concluida": False})
                    st.rerun()
                    
        with col_delete:
            if st.button("🗑️", key=f"del_{t['id']}", use_container_width=True):
                requests.delete(f"{API_URL}/tasks/{t['id']}")
                st.rerun()
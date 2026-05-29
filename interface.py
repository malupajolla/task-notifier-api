import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Task Notifier", page_icon="✅", layout="centered")

st.markdown("""
    <style>
        .title { font-size: 2.5rem; font-weight: 800; color: #4F8BF9; }
        .subtitle { color: #888; margin-bottom: 2rem; }
        .task-card { background: #f8f9fa; border-radius: 12px; padding: 1rem; margin-bottom: 0.5rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">✅ Task Notifier</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Gerencie suas tarefas e receba notificações no Telegram</div>', unsafe_allow_html=True)

# Criar tarefa
with st.expander("➕ Nova Tarefa", expanded=True):
    titulo = st.text_input("O que precisa ser feito?")
    destinatario = st.text_input("Seu Chat ID do Telegram:", value="7224724165")
    if st.button("Criar Tarefa", use_container_width=True):
        if titulo:
            resp = requests.post(f"{API_URL}/tasks/", params={"titulo": titulo, "destinatario": destinatario})
            if resp.status_code == 200:
                st.success("Tarefa criada e notificação enviada! 🎉")
                st.rerun()
        else:
            st.warning("Digite um título para a tarefa!")

st.divider()

# Listar tarefas
st.subheader("📋 Minhas Tarefas")
tarefas = requests.get(f"{API_URL}/tasks/").json()

if not tarefas:
    st.info("Nenhuma tarefa ainda. Crie uma acima! 👆")
else:
    for t in tarefas:
        col1, col2, col3 = st.columns([5, 2, 1])
        status = "✅" if t["concluida"] else "🔲"
        col1.markdown(f"**{status} {t['titulo']}**")
        
        if not t["concluida"]:
            if col2.button("Concluir", key=f"ok_{t['id']}", use_container_width=True):
                requests.put(f"{API_URL}/tasks/{t['id']}", params={"concluida": True})
                st.rerun()
        else:
            if col2.button("Reabrir", key=f"re_{t['id']}", use_container_width=True):
                requests.put(f"{API_URL}/tasks/{t['id']}", params={"concluida": False})
                st.rerun()

        if col3.button("🗑️", key=f"del_{t['id']}", use_container_width=True):
            requests.delete(f"{API_URL}/tasks/{t['id']}")
            st.rerun()
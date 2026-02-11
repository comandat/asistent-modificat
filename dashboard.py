import streamlit as st
import os, json, time

st.set_page_config(page_title="Nanobot Control Center", layout="wide")

WORK_DIR = "workspace"
TASKS_FILE = "workspace/TASKS.md"
PROGRESS_FILE = "workspace/PROGRESS.md"

if not os.path.exists(WORK_DIR): os.makedirs(WORK_DIR)
if not os.path.exists(TASKS_FILE): open(TASKS_FILE, 'w').close()

def load_tasks():
    with open(TASKS_FILE, 'r') as f:
        lines = f.readlines()
    tasks = {"TODO": [], "DOING": [], "DONE": []}
    current_section = None
    for line in lines:
        line = line.strip()
        if line == "## Backlog": current_section = "TODO"
        elif line == "## In Progress": current_section = "DOING"
        elif line == "## Completed": current_section = "DONE"
        elif line.startswith("- [ ]") and current_section:
            tasks[current_section].append(line[6:])
        elif line.startswith("- [x]") and current_section:
            tasks[current_section].append(line[6:])
    return tasks

def save_task(task_text):
    with open(TASKS_FILE, 'a') as f:
        f.write(f"\n- [ ] {task_text}")

st.title("🤖 Nanobot Dashboard")

tab1, tab2, tab3 = st.tabs(["Kanban Board", "Chat & Command", "Canvas Preview"])

with tab1:
    tasks = load_tasks()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("📝 To Do")
        for t in tasks["TODO"]: st.info(t)
    with c2:
        st.subheader("⚙️ In Progress")
        for t in tasks["DOING"]: st.warning(t)
    with c3:
        st.subheader("✅ Done")
        for t in tasks["DONE"]: st.success(t)

with tab2:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("New task or instruction..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        # Action: Add to TASKS.md
        save_task(prompt)
        response = f"Added task: **{prompt}** to Backlog."
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"): st.markdown(response)
        st.rerun()

    st.divider()
    uploaded_file = st.file_uploader("Upload Project Files")
    if uploaded_file:
        with open(os.path.join(WORK_DIR, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Saved {uploaded_file.name}")

with tab3:
    st.header("Canvas Preview (Live Site)")
    preview_path = os.path.join(WORK_DIR, "index.html")
    if os.path.exists(preview_path):
        with open(preview_path, "r") as f:
            html_content = f.read()
        st.components.v1.html(html_content, height=600, scrolling=True)
    else:
        st.info("No 'index.html' found in workspace yet. Ask Nanobot to build a site!")

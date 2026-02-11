import streamlit as st
import os, json, time, subprocess

st.set_page_config(page_title="Nanobot Control Center", layout="wide")

WORK_DIR = "workspace"
TASKS_FILE = "workspace/TASKS.md"
ENV_FILE = ".env"

if not os.path.exists(WORK_DIR): os.makedirs(WORK_DIR)
if not os.path.exists(TASKS_FILE): open(TASKS_FILE, 'w').close()

def load_env():
    """Load config from .env"""
    env = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            for line in f:
                if '=' in line:
                    key, val = line.strip().split('=', 1)
                    env[key] = val
    return env

def save_env(config):
    """Save config to .env"""
    with open(ENV_FILE, 'w') as f:
        for k, v in config.items():
            if v: f.write(f"{k}={v}\n")
    st.success("Configuration Saved! Restarting Nanobot...")
    time.sleep(1)
    st.rerun()

def check_nanobot():
    """Verify Nanobot installation"""
    try:
        result = subprocess.run(["nanobot", "version"], capture_output=True, text=True)
        return True, result.stdout.strip()
    except FileNotFoundError:
        return False, "Nanobot binary NOT FOUND in path."
    except Exception as e:
        return False, str(e)

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

# Main Layout
st.title("🤖 Nanobot Dashboard")

# Health Check
is_installed, version_msg = check_nanobot()
if is_installed:
    st.sidebar.success(f"✅ Engine Active: {version_msg}")
else:
    st.sidebar.error(f"❌ Engine Error: {version_msg}")

# Settings Check
current_env = load_env()
has_key = any([current_env.get("OPENAI_API_KEY"), current_env.get("ANTHROPIC_API_KEY"), current_env.get("GOOGLE_API_KEY")])

if not has_key:
    st.warning("⚠️ Nanobot is not configured. Please go to Settings.")

tab1, tab2, tab3, tab4 = st.tabs(["Kanban Board", "Chat & Command", "Canvas Preview", "⚙️ Settings"])

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
        if not has_key:
            st.error("Please configure API Key in Settings first!")
        elif not is_installed:
            st.error("Nanobot Engine is missing. Cannot execute.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            
            save_task(prompt)
            # Future: Execute nanobot run here via subprocess
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
        st.info("No 'index.html' found yet. Ask Nanobot to build one!")

with tab4:
    st.header("Configuration")
    st.info("Enter your API keys below. They are stored locally in .env")
    
    with st.form("config_form"):
        google_key = st.text_input("Google API Key (Gemini)", value=current_env.get("GOOGLE_API_KEY", ""), type="password")
        openai_key = st.text_input("OpenAI API Key", value=current_env.get("OPENAI_API_KEY", ""), type="password")
        anthropic_key = st.text_input("Anthropic API Key", value=current_env.get("ANTHROPIC_API_KEY", ""), type="password")
        
        st.divider()
        model = st.text_input("Model Name (Custom)", value=current_env.get("NANOBOT_MODEL", "gemini-1.5-pro-latest"), help="E.g., gemini-1.5-pro, gpt-4-turbo, claude-3-5-sonnet")
        
        submitted = st.form_submit_button("Save Configuration")
        if submitted:
            new_config = {
                "GOOGLE_API_KEY": google_key,
                "OPENAI_API_KEY": openai_key,
                "ANTHROPIC_API_KEY": anthropic_key,
                "NANOBOT_MODEL": model
            }
            save_env(new_config)

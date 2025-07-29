import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# ✅ Load environment variables
load_dotenv("apiroute.env")
api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE")

# ✅ Setup LLM
llm = ChatOpenAI(
    model_name="google/gemma-3n-e2b-it:free",
    temperature=0.7,
)

# ✅ Memory setup
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

# ✅ System prompt
system_prompt = (
    "You are Gremmy, a helpful, friendly AI chatbot created by Frederick using Google's Gemma model.\n"
    "- Introduce yourself **only once**, unless asked.\n"
    "- Be concise, polite, and informative.\n"
    "- Avoid repeating your background repeatedly.\n"
    "- For more about your creator: https://www.linkedin.com/in/j-frederick-paul-35801a179/"
)

# ✅ Inject system message only once
if "system_added" not in st.session_state:
    st.session_state.memory.chat_memory.add_message(SystemMessage(content=system_prompt))
    st.session_state.system_added = True

# ✅ Setup conversation chain
chat = ConversationChain(
    llm=llm,
    memory=st.session_state.memory,
    verbose=False
)

# ✅ Page config and title
st.set_page_config(page_title="Chatbot", layout="centered")
st.title("💬 Chat with Gremmy")

# ✅ Track and display history
if "history" not in st.session_state:
    st.session_state.history = []

for sender, msg in st.session_state.history:
    st.markdown(f"**{sender}:** {msg}")

# ✅ Input UI
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Talk to me", key="user_message")
    submitted = st.form_submit_button("Send")

# ✅ Handle submission
if submitted and user_input:
    st.session_state.history.append(("You", user_input))
    response = chat.run(user_input)
    st.session_state.history.append(("Gremmy", response.strip()))
    st.rerun()

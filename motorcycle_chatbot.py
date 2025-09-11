import os
import streamlit as st
from groq import Groq

st.set_page_config(page_title="Motorcycle Chatbot (Sri Lanka)", page_icon="🏍️")
st.title("🏍️ Motorcycle Chatbot (Sri Lanka)")

# -----------------------------
# Sidebar "About" Section
# -----------------------------
st.sidebar.header("ℹ️ About this Chatbot")
st.sidebar.info(
    """
    This chatbot is designed to answer questions about **motorcycles, scooters, and 
    the Sri Lankan motorcycle market**.  

    - 🤖 Powered by **Groq LLaMA 3.1 (8B Instant)**  
    - 🏍️ Specialized in **Sri Lankan motorcycle details**  
    - 🗑️ Use the **Clear Conversation** button to reset chat  
    - ❌ If you ask about unrelated topics, it will politely decline  

    💡 Try questions like:  
    - *What is the engine size of a Bajaj Pulsar 150?*  
    - *Popular scooters in Sri Lanka?*  
    - *What are the top motorcycle brands in Sri Lanka?*   
    """
)

# -----------------------------
# 1) Check API key
# -----------------------------
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error(
        "GROQ_API_KEY is not set.\n\n"
        "In your terminal, run:\n"
        "export GROQ_API_KEY='YOUR_KEY'\n\n"
        "Then restart the app."
    )
    st.stop()

# 2) Init Groq client
client = Groq(api_key=api_key)

# 3) System rule
SYSTEM_PROMPT = (
    "You are a helpful assistant that ONLY answers questions about motorcycles, "
    "scooters, and the Sri Lankan motorcycle market. If a question is unrelated, "
    "politely say you only answer motorcycle questions."
)

# 4) Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Clear chat button
if st.button("🗑️ Clear Conversation"):
    st.session_state["messages"] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    st.success("Conversation cleared!")

# 5) Render past messages (skip the system message)
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

# 6) Input → LLM → Output
user_input = st.chat_input("Ask me about motorcycles in Sri Lanka...")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state["messages"]
        )
    bot_reply = resp.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").write(bot_reply)

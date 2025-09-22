import os
import streamlit as st
from groq import Groq

# =============================
# Page Setup
# =============================
st.set_page_config(page_title="Motorcycle Chatbot (Sri Lanka)", layout="wide")

# Title
st.title("Motorcycle Chatbot (Sri Lanka)")

# =============================
# System Prompt (MUST be defined before Clear Button)
# =============================
SYSTEM_PROMPT = (
    "You are a helpful assistant that ONLY answers questions about motorcycles, "
    "scooters, and the Sri Lankan motorcycle market. "
    "If a question is unrelated, politely say you only answer motorcycle questions."
)

# -----------------------------
# Clear chat button (under title)
# -----------------------------
if st.button("🗑️ Clear Conversation"):
    st.session_state["messages"] = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.success("Conversation cleared!")

# =============================
# Sidebar
# =============================
with st.sidebar:
    st.header("ℹ️ About this Chatbot")
    st.info(
        """
        This chatbot is designed to **help you learn everything you don’t know 
        about motorcycles and scooters**. 
        
        - 🤖 **Powered by Groq LLaMA 3.1 (8B Instant)**  
        - 🏍️ Specialized in **Motorcycles**  
        - ❌ Non-motorcycle questions → will politely decline.  

        💡 Example Questions:  
        - What are the top motorcycle brands in Sri Lanka?  
        - Popular scooters in Sri Lanka?  
        - What is the engine size of a Bajaj Pulsar 150?  
        """
    )
    st.markdown("---")
    st.markdown("**Developer:** M R K Karunathilaka")
    st.markdown("**Version:** 1.0.0")
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: grey;'>© 2025 Motorcycle Chatbot</p>",
        unsafe_allow_html=True,
    )

# =============================
# API Key
# =============================
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error(
        "❌ GROQ_API_KEY is not set.\n\n"
        "In your terminal, run:\n"
        "```bash\nexport GROQ_API_KEY='YOUR_KEY'\n```"
    )
    st.stop()

# =============================
# Init Client
# =============================
client = Groq(api_key=api_key)

# =============================
# Session State for Chat
# =============================
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": SYSTEM_PROMPT}]

# =============================
# Chat Display
# =============================
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg["content"])

# =============================
# User Input
# =============================
user_input = st.chat_input("Ask me about motorcycles in Sri Lanka...")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Generate response
    with st.spinner("🤔 Thinking..."):
        try:
            resp = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=st.session_state["messages"]
            )
            bot_reply = resp.choices[0].message.content
        except Exception as e:
            bot_reply = f"⚠️ Error: {str(e)}"

    # Show assistant reply
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot_reply)

    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
    

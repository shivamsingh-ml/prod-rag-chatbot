import streamlit as st
import requests

API_UPLOAD_URL = "http://backend:8000/upload-pdf/"
API_CHAT_URL = "http://backend:8000/chat"
API_DELETE_COLLECTION_URL = "http://backend:8000/delete-collection/"


st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")

if "session_started" not in st.session_state:
    st.session_state.session_started = False
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🤖 RAG Chatbot")

if not st.session_state.session_started:
    uploaded_file = st.file_uploader("📄 Upload a PDF", type="pdf")

    if uploaded_file:
        st.success("✅ PDF uploaded successfully. Ready to start session.")

        if st.button("🚀 Start Session"):
            with st.spinner("Starting session..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    response = requests.post(API_UPLOAD_URL, files=files)
                    response.raise_for_status()
                    data = response.json()
                    session_id = data.get("session_id")
                    if session_id:
                        st.session_state.session_id = session_id
                        st.session_state.session_started = True
                        st.success("🎉 Session started!")
                        st.rerun()
                    else:
                        st.warning("⚠️ No session ID returned.")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Error: {e}")

if st.session_state.session_started:
    st.subheader("💬 Chat with your document")
    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown(
        f"<div style='font-size: 1.1rem; padding-top: 0.4rem;'><b> Session ID:</b> <code>{st.session_state.session_id}</code></div>",
        unsafe_allow_html=True
    )

    with col2:
        if st.button("❌ End Session"):
            try:
                requests.post(API_DELETE_COLLECTION_URL, json={
                    "session_id": st.session_state.session_id
                })
            except Exception as e:
                st.warning(f"⚠️ Failed to delete session collection: {e}")

            st.session_state.session_started = False
            st.session_state.session_id = None
            st.session_state.chat_history = []
            st.rerun()
        
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your question...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            response = requests.post(API_CHAT_URL, json={
                "query": user_input,
                "session_id": st.session_state.session_id
            })
            response.raise_for_status()
            data = response.json()
            answer = data.get("answer", "⚠️ No answer returned.")
        except Exception as e:
            answer = f"❌ Error: {e}"

        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

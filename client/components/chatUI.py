import streamlit as st
from utils.api import ask_question

def render_chat():
    # Custom CSS for styling
    st.markdown("""
    <style>
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .chat-header h2 {
        margin: 0;
        font-size: 1.5rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 15px 15px 5px 15px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .assistant-message {
        background: #f8f9fa;
        color: #333;
        padding: 15px;
        border-radius: 15px 15px 15px 5px;
        margin: 10px 0;
        max-width: 80%;
        margin-right: auto;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .sources-container {
        background: #e8f4fd;
        border: 1px solid #bee5eb;
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .sources-title {
        color: #0c5460;
        font-weight: 600;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .source-item {
        background: white;
        padding: 8px 12px;
        margin: 5px 0;
        border-radius: 6px;
        border-left: 3px solid #667eea;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
    }
    .stChatInput {
        margin-top: 20px;
    }
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render existing chat history with custom styling
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "user":
                st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)

    # Input and response
    user_input = st.chat_input("Type your question here...")
    
    if user_input:
        # Display user message
        with st.chat_message("user"):
            st.markdown(f'<div class="user-message">{user_input}</div>', unsafe_allow_html=True)
        
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get response from API
        with st.spinner("🤔 Thinking..."):
            response = ask_question(user_input)
        
        if response.status_code == 200:
            data = response.json()
            answer = data["answer"]
            sources = data.get("sources", [])
            
            # Display assistant message
            with st.chat_message("assistant"):
                st.markdown(f'<div class="assistant-message">{answer}</div>', unsafe_allow_html=True)
                
                # Display sources if available
                if sources:
                    st.markdown("""
                    <div class="sources-container">
                        <div class="sources-title">
                            📄 Document Sources
                        </div>
                    """, unsafe_allow_html=True)
                    
                    for src in sources:
                        st.markdown(f'<div class="source-item">{src}</div>', unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        else:
            error_msg = st.markdown(
                f'<div class="error-message">Error: {response.text}</div>', 
                unsafe_allow_html=True
            )
            st.session_state.messages.append({"role": "assistant", "content": f"Error: {response.text}"})

    # Add some helpful tips
    if not st.session_state.messages:
        st.markdown("""
        <div style="background: #f0f2f6; padding: 20px; border-radius: 10px; margin-top: 20px;">
            <h4>💡 Tips for better responses:</h4>
            <ul>
                <li>Ask specific STEM questions</li>
                <li>Reference particular sections or topics</li>
                <li>Request sources for verification</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
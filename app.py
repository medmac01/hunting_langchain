import streamlit as st
from agents import investigator
# from agents_openai_fc import investigator

st.title('Cyber Hunter!')
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = investigator.invoke(prompt)
    msg = response["output"]

    # print(response['intermediate_steps'])
    
    # If there's an existing assistant message, update it with the new response
    if st.session_state.messages[-1]["role"] == "assistant":
        st.session_state.messages[-1]["content"] = msg
    else:
        st.session_state.messages.append({"role": "assistant", "content": msg})

    st.chat_message("assistant").write(msg)

# Add a button to regenerate response
if st.button("Regenerate Response"):
    st.session_state.messages.pop()  # Remove the latest assistant message
    prompt = st.session_state.messages[-1]["content"]  # Retrieve user's last input
    with st.spinner("Searching..."):
        response = investigator.invoke(prompt)
        msg = response["output"]
        
        # If there's an existing assistant message, update it with the new response
        if st.session_state.messages[-1]["role"] == "assistant":
            st.session_state.messages[-1]["content"] = msg
        else:
            st.session_state.messages.append({"role": "assistant", "content": msg})

        st.chat_message("assistant").write(msg)

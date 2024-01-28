import streamlit as st
import utils
import json

# Assuming utils and other necessary imports are correctly defined

st.set_page_config(page_title="Chatbot", page_icon="💬")
st.header('Basic Chatbot')
st.write('Allows users to interact with the LLM')

class Chatbot:

    def __init__(self):
        utils.configure_openai_api_key()
        self.openai_model = "gpt-3.5-turbo"
        self.custom_responses = [
            "This is the first custom response.",
            "Here's another response, tailored to your second question.",
            "Continuing our conversation, here's the third response.",
            # Add more responses as needed
        ]
        # Initialize response_index in session_state if it doesn't exist
        if 'response_index' not in st.session_state:
            st.session_state.response_index = 0

    def setup_chain(self):
        llm = OpenAI(model_name=self.openai_model, temperature=0, streaming=True)
        chain = ConversationChain(llm=llm, verbose=True)
        return chain
    
    @utils.enable_chat_history_profile
    def context_builder(self):
        user_query = st.chat_input(placeholder="Type your question here!")
        if user_query:
            utils.display_msg(user_query, 'user')
            with st.chat_message("assistant"):
                if st.session_state.response_index < len(self.custom_responses):
                    # Get the next custom response from the list using session_state
                    custom_response = self.custom_responses[st.session_state.response_index]
                    st.session_state.response_index += 1
                else:
                    # Once all responses are used up, return "Thank you"
                    custom_response = "Thank you"
                    self.save_messages_to_file(st.session_state.messages)
                    # Reset the index if you want to start over, or disable the input if not
                    # st.session_state.response_index = 0
                    # To disable the input, you could use something like st.stop()

                # Display the custom response
                st.write(custom_response)

                # Add the custom response to the session state messages
                st.session_state.messages.append({"role": "assistant", "content": custom_response})

    def save_messages_to_file(self, messages):
        # Save the messages to a file in JSON format
        with open('chat_history.json', 'w') as f:
            json.dump(messages, f, indent=2)

if __name__ == "__main__":
    obj = Chatbot()
    obj.context_builder()

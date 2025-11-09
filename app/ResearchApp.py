import streamlit as st
import requests
import json
import uuid
import time

# Set page config
st.set_page_config(
    page_title="Research Assistant",
    page_icon="�",
    layout="centered"
)

# Constants
#API_BASE_URL = "http://localhost:8000" if on localhost
API_BASE_URL = "http://0.0.0.0:8080"
APP_NAME = "multi_tool_agent"

# Initialize session state variables
if "user_id" not in st.session_state:
    st.session_state.user_id = f"user-{uuid.uuid4()}"
    
if "session_id" not in st.session_state:
    st.session_state.session_id = None
    
if "messages" not in st.session_state:
    st.session_state.messages = []

def create_session():
    """
    Create a new session with the speaker agent.
    
    This function:
    1. Generates a unique session ID based on timestamp
    2. Sends a POST request to the ADK API to create a session
    3. Updates the session state variables if successful
    
    Returns:
        bool: True if session was created successfully, False otherwise
    
    API Endpoint:
        POST /apps/{app_name}/users/{user_id}/sessions/{session_id}
    """
    session_id = f"session-{int(time.time())}"
    response = requests.post(
        f"{API_BASE_URL}/apps/{APP_NAME}/users/{st.session_state.user_id}/sessions/{session_id}",
        headers={"Content-Type": "application/json"},
        data=json.dumps({})
    )
    
    if response.status_code == 200:
        st.session_state.session_id = session_id
        st.session_state.messages = []
        return True
    else:
        st.error(f"Failed to create session: {response.text}")
        return False

def send_message(message):
    """
    Send a message to the speaker agent and process the response.
    
    This function:
    1. Adds the user message to the chat history
    2. Sends the message to the ADK API
    3. Processes the response to extract text and audio information
    4. Updates the chat history with the assistant's response
    
    Args:
        message (str): The user's message to send to the agent
        
    Returns:
        bool: True if message was sent and processed successfully, False otherwise
    
    API Endpoint:
        POST /run
        
    Response Processing:
        - Parses the ADK event structure to extract text responses
        - Looks for text_to_speech function responses to find audio file paths
        - Adds both text and audio information to the chat history
    """
    if not st.session_state.session_id:
        st.error("No active session. Please create a session first.")
        return False
    
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": message})
    
    # Send message to API
    response = requests.post(
        f"{API_BASE_URL}/run",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "appName": APP_NAME,
            "userId": st.session_state.user_id,
            "sessionId": st.session_state.session_id,
            "newMessage": {
                "role": "user",
                "parts": [{
                    "text": message
                }]
            },
            "streaming": True
        })
    )
    
    if response.status_code != 200:
        error_detail = ""
        try:
            error_data = response.json()
            error_detail = error_data.get("detail", response.text)
        except:
            error_detail = response.text
        st.error(f"Error {response.status_code}: {error_detail}")
        return False
    
    try:
        # Process the response
        response_data = response.json()
        assistant_message = None
        
        # Handle different response formats
        if isinstance(response_data, list):
            # Combine all response parts into a single message
            message_parts = []
            final_message = None
            
            for event in response_data:
                if isinstance(event, dict):
                    content = ""
                    # Try different possible response structures
                    if "content" in event and isinstance(event["content"], str):
                        content = event["content"]
                    elif "content" in event and isinstance(event["content"], dict):
                        if "parts" in event["content"]:
                            for part in event["content"]["parts"]:
                                if isinstance(part, dict) and "text" in part:
                                    content = part["text"]
                    
                    # Skip content that looks like JSON
                    if content.strip().startswith('{') or content.strip().startswith('"report"'):
                        continue
                        
                    # Skip internal dialogue messages
                    if any(phrase in content for phrase in [
                        "I understand",
                        "Okay, I will",
                        "Great! I'm glad",
                        "Okay, great!",
                        "No further action",
                        "Understood.",
                        "I will await"
                    ]):
                        continue
                    
                    # Check if this is a final evaluation or recommendation message
                    if any(phrase in content for phrase in [
                        "Final Evaluation: Approved",
                        "Final Recommendation:",
                        "Final Assessment:"
                    ]):
                        # Only keep content up to and including the final message
                        for phrase in [
                            "Final Evaluation: Approved",
                            "Final Recommendation:",
                            "Final Assessment:"
                        ]:
                            if phrase in content:
                                final_idx = content.find(phrase) + len(content.split(phrase)[0]) + len(phrase)
                                final_message = content[:final_idx].strip()
                                break
                        break
                    elif "functionCall" in event:
                        # Capture function calls as part of the response
                        func_call = event["functionCall"]
                        message_parts.append(f"Planning step: {func_call.get('name', 'Unknown function')}")
                    else:
                        # Only add non-empty, meaningful content
                        if content.strip() and not content.strip().startswith('{'):
                            message_parts.append(content)
            
            if final_message:
                assistant_message = final_message
            elif message_parts:
                assistant_message = "\n".join(message_parts)
        else:
            # Handle non-streaming format
            if isinstance(response_data, dict):
                if "content" in response_data:
                    assistant_message = response_data["content"]
                elif "newMessage" in response_data:
                    parts = response_data["newMessage"].get("parts", [])
                    if parts and isinstance(parts[0], dict) and "text" in parts[0]:
                        assistant_message = parts[0]["text"]
        
        if not assistant_message:
            st.error("Could not extract assistant message from response")
    except json.JSONDecodeError as e:
        st.error(f"Error decoding response: {str(e)}")
        return False
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return False
    
    # Add assistant response to chat
    if assistant_message:
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    
    return True

# UI Components
st.title("� Research Assistant")

# Sidebar for session management
with st.sidebar:
    st.header("Session Management")
    
    if st.session_state.session_id:
        st.success(f"Active session: {st.session_state.session_id}")
        if st.button("➕ New Session"):
            create_session()
    else:
        st.warning("No active session")
        if st.button("➕ Create Session"):
            create_session()
    
    st.divider()
    st.caption("This app interacts with the Research Assistant via the ADK API Server.")
    st.caption("Make sure the ADK API Server is running on port 8000.")

# Chat interface
st.subheader("Research Conversation")

# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])

# Input for new messages
if st.session_state.session_id:  # Only show input if session exists
    user_input = st.chat_input("Ask your research question...")
    if user_input:
        with st.status("Researching your question...", expanded=True) as status:
            st.write("Processing your request...")
            success = send_message(user_input)
            if success:
                status.update(label="Response received!", state="complete")
            else:
                status.update(label="Error occurred", state="error")
        st.rerun()  # Rerun to update the UI with new messages
else:
    st.info("👈 Create a session to start chatting")
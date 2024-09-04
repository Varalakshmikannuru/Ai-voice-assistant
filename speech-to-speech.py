import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai 

# Replace this with your actual Google API key
GOOGLE_API_KEY = "AIzaSyCsXO30QbeuW42Qn6GlfhTpljjr_E1d3qo"

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Initialize session state for chat history if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Configure LLM
def llm(text): 
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(text)
    return response.text.lower()

# Speech recognition function
def recognize_speech_from_microphone(listening_placeholder):
    with sr.Microphone() as source:
        listening_placeholder.info("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        try:
            audio = recognizer.record(source, duration=5)
            text = recognizer.recognize_google(audio)
            st.session_state.chat_history.append(f"You: {text}")
            listening_placeholder.empty()  # Clear the "Listening..." message
            return text
        except sr.UnknownValueError:
            listening_placeholder.error("🚫 Could not understand the audio.")
        except sr.RequestError:
            listening_placeholder.error("⚠️ Could not request results from the service.")
        return None

# Text-to-speech function
def speak_text(text):
    if tts_engine._inLoop:  # Check if the event loop is already running
        tts_engine.endLoop()  # End the loop if it's running
    tts_engine.say(text)
    tts_engine.runAndWait()

# Streamlit app UI
st.set_page_config(page_title="AI Voice Assistant1", page_icon="🗣️")

# Custom CSS styles
st.markdown(
    """
    <style>
    body {
        background-size: cover;
        font-family: "Arial", sans-serif;
        color: #f4f4f4;
    }

    /* Title and Header */
    .main > div {
        padding-top: 20px;
    }
    .css-10trblm {
        font-size: 2em;
        color: #ffffff;
        position: sticky;
        top: 0;
        background-color: rgba(0, 0, 0, 0.7);
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 100;
    }

    /* Button Styling */
    .stButton button {
        border: 2px solid #ff5722;
    }
    .stButton button:hover {
        color: #ff5722;
        transform: scale(1.05);
    }

    /* Chat Bubble Styling */
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 15px;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }
    .chat-bubble-user {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 10px 15px;
        margin-bottom: 10px;
        border-radius: 20px 20px 20px 0;
        text-align: left;
        color: #333;
    }
    .chat-bubble-bot {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 10px 15px;
        margin-bottom: 10px;
        border-radius: 20px 20px 0 20px;
        text-align: left;
        color: #f4f4f4;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.5);
        border-radius: 8px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.7);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.title("🗣️ AI Voice Assistant")
st.markdown("*Engage in a voice-based conversation with AI. Click the button below to start talking!*")

# Divider line
st.markdown("---")

# Chat Interface
st.write("### Conversation History")
chat_expander = st.expander("Click to View Chat History", expanded=True)

with chat_expander:
    st.write('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.chat_history:
        if message.startswith("You:"):
            st.markdown(f'<div class="chat-bubble-user">{message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-bot">{message}</div>', unsafe_allow_html=True)
    st.write('</div>', unsafe_allow_html=True)

# Start Talking Button
if st.button("🎤 Start Talking"):
    listening_placeholder = st.empty()  # Placeholder for "Listening..." message
    recognized_text = recognize_speech_from_microphone(listening_placeholder)
    if recognized_text:
        with st.spinner("Processing..."):
            processed_text = llm(recognized_text)
            st.session_state.chat_history.append(f"Bot: {processed_text}")
        
        # Update chat history and speak response
        with chat_expander:
            st.write('<div class="chat-container">', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble-bot">{processed_text}</div>', unsafe_allow_html=True)
            st.write('</div>', unsafe_allow_html=True)
        speak_text(processed_text)

# Footer
st.markdown("---")
st.write("🤖 *AI Voice Assistant* - Powered by Google Generative AI")



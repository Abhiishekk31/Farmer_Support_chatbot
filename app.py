import os
import json
import groq
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from dotenv import load_dotenv
import tempfile

# Load environment variables
load_dotenv()

### **🤖 Generate Chatbot Responses Using Groq**
def get_answer(conversation_history):
    """Generates a response from Groq API based on conversation history."""

    # Convert conversation history to JSON format
    history_json = json.dumps(conversation_history, indent=2)

    # Extract latest user input
    latest_input = conversation_history[-1]["content"] if conversation_history else "Hello"

    # Define system prompt
    SYSTEM_PROMPT = f"""You are a knowledgeable and empathetic AI consultant specializing in **agriculture and farming**. Your goal is to support farmers by providing accurate, practical, and easy-to-understand solutions for their farming-related concerns.  

### **CONVERSATION GUIDELINES:**  
- Always maintain a **respectful, patient, and supportive tone**  
- Offer **scientific yet simple explanations** that farmers can easily apply  
- Keep responses **concise, practical, and action-oriented**  
- Support queries with **data, best practices, and latest agricultural techniques**  
- Use **bilingual communication (English and Hindi)** for better accessibility  
- Remember previous interactions to provide **personalized recommendations**  

### **RESPONSE STRUCTURE:**  
1. **Acknowledge the farmer’s concern and validate their question**  
2. **Refer to any relevant past conversation details to maintain continuity**  
3. **Ask follow-up questions if more details are needed (e.g., soil type, climate, crop variety, etc.)**  
4. **Provide clear, step-by-step solutions or recommendations**  
5. **Suggest government schemes, subsidies, or resources where applicable**  
6. **End with encouragement and an invitation to ask further questions**  

### **EXPERTISE AREAS:**  
- **Crop Selection & Yield Optimization** (best crops for different climates and soil types)  
- **Pest & Disease Management** (identification and organic/chemical treatments)  
- **Soil Health & Fertilization** (nutrient requirements, organic farming, soil testing)  
- **Irrigation Techniques** (drip irrigation, rainwater harvesting, efficient water use)  
- **Weather & Climate Advisory** (seasonal crop planning, climate adaptation)  
- **Farm Mechanization** (use of tractors, machinery, modern tools)  
- **Government Subsidies & Schemes** (PM Kisan Yojana, crop insurance, financial aid)  
- **Market & Pricing Guidance** (best selling times, direct-to-market strategies)  

### **INTERACTION STYLE:**  
*"Imagine I'm an experienced agricultural advisor who understands your farming challenges and wants to help you make informed decisions. Let’s work together to improve your farm’s productivity!"*  

### **KEY PHRASES IN ENGLISH:**  
- "I understand your concern about [specific issue] and have some suggestions for you…"  
- "Based on your soil and climate, the best approach would be…"  
- "Have you considered using [technique] to improve yield?"  
- "Let’s break this down into practical steps…"  

### **KEY PHRASES IN MARATHI:**  
-"मी समजू शकतो/शकते की [समस्या] तुमच्यासाठी आव्हानात्मक आहे…"
-"तुमच्या माती आणि हवामानाच्या आधारावर, सर्वोत्तम मार्ग असेल…"
-"तुम्ही [तंत्रज्ञान] वापरण्याचा विचार केला आहे का?"
-"चला याला सोप्या आणि प्रभावी पद्धतींमध्ये समजून घेऊ…" 

### **CRITICAL SAFETY PROTOCOLS:**  
- **Do NOT provide medical advice for humans or animals** (redirect to a vet or doctor)  
- **Do NOT give financial guarantees** (e.g., exact crop prices or guaranteed profits)  
- **Do NOT discuss non-agriculture topics** (strictly respond to farming-related queries)  

### **PROHIBITED RESPONSES:**  
- Generic or vague advice without a clear solution  
- Non-farming discussions (e.g., politics, religion, unrelated health issues)  
- Unverified claims or misleading information  

Based on ```{latest_input}``` and ```{history_json}```, formulate a response that provides **practical, accurate, and relevant farming advice** while ensuring clarity and accessibility.  
"""

    # Call Groq API
    client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Adjust based on Groq’s available models
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
    )

    return response.choices[0].message.content

### **🎤 Voice Input Handling**
def recognize_speech():
    """Captures and converts speech input to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "Speech Recognition service unavailable"

### **🔊 Convert AI Response to Audio**
def text_to_speech(response_text):
    """Converts text to speech and plays the audio."""
    tts = gTTS(text=response_text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        tts.save(temp_audio.name)
        return temp_audio.name

### **💬 Streamlit Interface**
st.title("🌾 Farmer Consultant AI")
st.write("Ask any farming-related question and get expert advice.")

if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Display chat history
for message in st.session_state.conversation:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**AI:** {message['content']}")

# User input
user_input = st.text_input("Your question:", "")
voice_input = st.button("🎤 Speak")
if voice_input:
    user_input = recognize_speech()
    st.text(f"You said: {user_input}")

if st.button("Ask AI") and user_input:
    st.session_state.conversation.append({"role": "user", "content": user_input})
    ai_response = get_answer(st.session_state.conversation)
    st.session_state.conversation.append({"role": "assistant", "content": ai_response})
    
    # Convert AI response to audio
    audio_file = text_to_speech(ai_response)
    st.audio(audio_file, format="audio/mp3")
    st.rerun()

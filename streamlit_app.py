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

def get_answer(conversation_history):
    """Generates a response from Groq API based on conversation history."""
    
    history_json = json.dumps(conversation_history, indent=2)
    latest_input = conversation_history[-1]["content"] if conversation_history else "Hello"

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

### **KEY PHRASES IN HINDI:**  
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
    
    client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
    )
    
    return response.choices[0].message.content

# Voice Input Handling
def recognize_speech():
    """Captures and converts speech input to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening... Press 'Stop Listening' to finish.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "Speech Recognition service unavailable"

# Convert AI Response to Audio
def text_to_speech(response_text):
    """Converts text to speech and plays the audio."""
    tts = gTTS(text=response_text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        tts.save(temp_audio.name)
        return temp_audio.name

# Streamlit UI
st.title("Farmer Consultant Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.listening = False

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

col1, col2 = st.columns([1, 1])

with col1:
    user_input = st.chat_input("Type your message...")
with col2:
    if st.session_state.listening:
        if st.button("⏹ Stop Listening"):
            st.session_state.listening = False
    else:
        if st.button("🎤 Start Listening"):
            st.session_state.listening = True
            user_input = recognize_speech()
            st.text(f"You said: {user_input}")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)
    
    response = get_answer(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    with st.chat_message("assistant"):
        st.write(response)
    
    audio_file = text_to_speech(response)
    st.audio(audio_file, format="audio/mp3")
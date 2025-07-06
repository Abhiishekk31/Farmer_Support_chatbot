# 🌾 Farmer Support Chatbot

An intelligent AI-powered chatbot designed to provide expert agricultural advice and support to farmers. Built with Streamlit and powered by Groq's LLM API, this application offers both text and voice interaction capabilities to make farming guidance accessible and user-friendly.

## 🚀 Features

### 🤖 AI-Powered Agricultural Consulting
- **Expert Farming Advice**: Get personalized recommendations for crop selection, pest management, soil health, and more
- **Bilingual Support**: Responses in both English and Hindi for better accessibility
- **Context-Aware Conversations**: Remembers previous interactions for personalized recommendations
- **Scientific Accuracy**: Based on latest agricultural research and best practices

### 🎤 Voice Interaction
- **Speech-to-Text**: Ask questions using your voice for hands-free operation
- **Text-to-Speech**: Listen to AI responses as audio for better accessibility
- **Real-time Voice Recognition**: Instant speech processing and conversion

### 💬 User-Friendly Interface
- **Streamlit Web App**: Clean, intuitive web interface
- **Chat-like Experience**: Natural conversation flow with message history
- **Responsive Design**: Works on desktop and mobile devices
- **Session Management**: Maintains conversation context throughout the session

### 🌱 Agricultural Expertise Areas
- **Crop Selection & Yield Optimization**
- **Pest & Disease Management**
- **Soil Health & Fertilization**
- **Irrigation Techniques**
- **Weather & Climate Advisory**
- **Farm Mechanization**
- **Government Schemes & Subsidies**
- **Market & Pricing Guidance**

## 📋 Prerequisites

Before running this application, ensure you have:

- **Python 3.7+** installed on your system
- **Microphone access** for voice input functionality
- **Internet connection** for API calls and speech recognition
- **Groq API Key** (sign up at [groq.com](https://groq.com))

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Farmer_Support_chatbot-main
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

## 🚀 Usage

### Option 1: Run the main Streamlit app
```bash
streamlit run streamlit_app.py
```

### Option 2: Run the alternative app version
```bash
streamlit run app.py
```

### Using the Application

1. **Text Input**: Type your farming-related question in the chat input field
2. **Voice Input**: Click the microphone button to speak your question
3. **Get Expert Advice**: The AI will provide detailed, practical farming guidance
4. **Listen to Responses**: Audio playback of AI responses is available
5. **Continue Conversation**: Ask follow-up questions for more specific advice

## 📁 Project Structure

```
Farmer_Support_chatbot-main/
├── app.py                 # Main Streamlit application
├── streamlit_app.py       # Alternative Streamlit app with chat interface
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── .env                  # Environment variables (create this file)
```

## 🔧 Technical Details

### Dependencies
- **streamlit**: Web application framework
- **groq**: LLM API client for AI responses
- **speechrecognition**: Speech-to-text conversion
- **gtts**: Text-to-speech conversion
- **python-dotenv**: Environment variable management

### API Integration
- **Groq LLM API**: Powers the AI responses using the Llama-3.3-70b-versatile model
- **Google Speech Recognition**: Handles voice input processing
- **Google Text-to-Speech**: Converts AI responses to audio

### Safety Protocols
The chatbot includes built-in safety measures:
- **No Medical Advice**: Redirects health-related queries to professionals
- **No Financial Guarantees**: Avoids making profit predictions
- **Agriculture Focus**: Strictly responds to farming-related topics only

## 🌟 Key Features Explained

### Intelligent Response System
The AI is trained with a comprehensive system prompt that includes:
- Agricultural expertise guidelines
- Bilingual communication capabilities
- Safety protocols and prohibited responses
- Structured response format for clarity

### Voice Processing Pipeline
1. **Speech Recognition**: Captures audio input using microphone
2. **Noise Reduction**: Adjusts for ambient noise
3. **Text Conversion**: Converts speech to text using Google's API
4. **Response Generation**: Processes through Groq's LLM
5. **Audio Output**: Converts response back to speech

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Bug fixes
- Feature enhancements
- Documentation improvements
- Localization support for additional languages

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Groq** for providing the LLM API
- **Streamlit** for the web application framework
- **Google** for speech recognition and text-to-speech services
- **Agricultural experts** whose knowledge informs the AI responses

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with detailed description
3. Include system information and error logs

---

**Happy Farming! 🌱** 

*This chatbot is designed to support farmers with practical, science-based agricultural advice. Always consult local agricultural experts for region-specific recommendations.* 

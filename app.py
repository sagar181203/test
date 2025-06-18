import streamlit as st
from openai import OpenAI
import pyttsx3
import speech_recognition as sr

# Fix for pyttsx3 COM initialization error on Windows
try:
    import pythoncom
    pythoncom.CoInitialize()
except ImportError:
    pass

# OpenAI API key using new Client API (v1.x+)
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = "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"

client = OpenAI(api_key=api_key)

# Streamlit page config
st.set_page_config(page_title="Voite Bot", layout="wide")

# Custom CSS for better UI
st.markdown("""
    <style>
    .main { background-color: #f7f9fa; }
    .stButton>button {
        background: linear-gradient(90deg, #5A9FFF 0%, #6EE7B7 100%);
        color: white; border-radius: 8px; font-weight: bold; padding: 0.5em 2em; margin-top: 1em;
    }
    .response-box {
        background: #f8fafc; border-radius: 10px; padding: 1.5em; margin-top: 1em;
        box-shadow: 0 2px 8px rgba(90,159,255,0.08); font-size: 1.15em; color: #1a202c;
        font-weight: 600; border: 1.5px solid #5A9FFF;
    }
    .question-box {
        background: #e6f7ff; border-radius: 10px; padding: 0.8em; margin-top: 0.5em;
        font-size: 1.08em; color: #1a202c; font-weight: 700; border: 1.5px solid #5A9FFF;
    }
    .info-visible {
        background: #e3f8ff !important; color: #1a2b3c !important; font-weight: 700 !important;
        padding: 0.7em 1.2em !important; border-radius: 8px !important; margin-bottom: 0.5em !important;
        border: 1.5px solid #5A9FFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://img.icons8.com/color/96/000000/robot-2.png", width=72)
st.sidebar.title("Voice Bot")
st.sidebar.markdown("""
**How to use:**
- Choose to speak or type your question.
- Get instant answers with voice!
- Powered by ChatGPT (OpenAI) for all questions.

**Sample Questions:**
  - What should we know about your life story?
  - What's your number one superpower?
  - What are the top three areas you'd like to grow in?
  - What misconception do your coworkers have about you?
  - How do you push your boundaries and limits?
    
""")

# Get response function (updated for new OpenAI SDK)
def get_response(question):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": (
                    "You are Sagar Kumar, a real person. "
                    "You are originally from India, belong to Bihar, and currently based in Karnataka for your education and work. "
                    "You have a Bachelor's degree in Artificial Intelligence and Machine Learning from PES Institute of Technology and Management, with an aggregate CGPA or GPA of 9.14/10. "
                    "You are highly passionate about AI & ML, with hands-on experience in Deep Learning, NLP, Computer Vision, and GenAI technologies. "
                    "You have completed multiple internships, including a Deep Learning Internship at ResoluteAI Software Pvt Ltd (where you worked on foundations of ML and deep learning models and real-world AI models), Infosys Springboard Internship 5.0, and Dhee Coding Lab (training on HTML, CSS, Core Java, DSA, and programming logic). "
                    "You have worked on several projects such as: language translation system (Kannada to English with voice cloning), speech-to-text transcription, emotion detection using deep learning, face recognition attendance system, lip-syncing using Wav2Lip, and real-time EV fleet monitoring and predictive analytics. "
                    "You have strong technical skills in Python, TensorFlow, PyTorch, scikit-learn, LangChain, LlamaIndex, Hugging Face, AWS Bedrock, Anthropic models, GANs, Postman API, SQL, Flask, FastAPI, and Streamlit. "
                    "You are also proficient in data structures, algorithms, networking, microprocessors, and software engineering concepts. "
                    "You have been among the Top 10 rank holders of your university and are a department topper. "
                    "You hold multiple certifications, including Infosys Springboard Certifications, Dhee Coding Lab Certification, and certifications in AI, Machine Learning, and Deep Learning. "
                    "Your programming language skills include Python, Java, C, SQL, and JavaScript. "
                    "Outside of academics, you enjoy reading tech blogs, articles, cooking, spending time with friends and family, and exploring new technologies. "
                    "You always answer questions from your own personal perspective based on your knowledge, skills, experience, projects, and achievements. "
                    "Always reply as yourself, in the first person, naturally and authentically. "
                    "Never mention AI, assistants, or that you are generating a response. "
                    "Speak as if you are directly chatting or talking."
                )},
                {"role": "user", "content": question}
            ]
        )
        content = response.choices[0].message.content
        return content.strip() if content else "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"Sorry, I couldn't get an answer from ChatGPT. Error: {str(e)}"

# Text-to-speech function
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"Text-to-Speech error: {e}")

# Main Streamlit app
def main():
    st.markdown("<h1 style='text-align:center;color:#5A9FFF;'>🎙️ Voite Bot</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#6EE7B7; font-size:1.2em;'>Ask me interview questions and I'll reply with voice and text!</div>", unsafe_allow_html=True)
    st.write("")

    col1, col2 = st.columns([1, 1])
    with col1:
        option = st.radio("Choose input method:", ["🎤 Speak", "⌨️ Type"], index=0)

    user_question, response, error = None, None, None

    if option == "🎤 Speak":
        if st.button("🎤 Record and Ask"):
            r = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    st.markdown('<div class="info-visible">Listening... Please speak clearly into your mic.</div>', unsafe_allow_html=True)
                    r.adjust_for_ambient_noise(source, duration=1)
                    with st.spinner("Listening..."):
                        audio = r.listen(source, timeout=5, phrase_time_limit=10)
                    user_question = r.recognize_google(audio)
                    st.markdown(f'<div class="question-box">You asked: <b>{user_question}</b></div>', unsafe_allow_html=True)
                    response = get_response(user_question)
            except sr.UnknownValueError:
                error = "Sorry, I couldn't understand your voice."
            except sr.RequestError as e:
                error = f"Speech Recognition error: {e}"
            except Exception as e:
                error = f"Microphone or audio error: {e}"

    elif option == "⌨️ Type":
        user_question = st.text_input("Type your question here:")
        if st.button("💬 Ask") and user_question:
            st.markdown(f'<div class="question-box">You asked: <b>{user_question}</b></div>', unsafe_allow_html=True)
            response = get_response(user_question)

    if error:
        st.markdown(f'<div class="response-box" style="color:#b91c1c;background:#ffeaea;border:1.5px solid #ff6a6a;">{error}</div>', unsafe_allow_html=True)
    if response:
        st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)
        speak(response)

if __name__ == "__main__":
    main()

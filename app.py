import streamlit as st
from main import SmartTranslator

st.title("Machine Translator")

@st.cache_resource
def get_translator():
    return SmartTranslator()

try:
    translator = get_translator()
except Exception as e:
    st.error(f"Error loading models: {e}")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input")
    source_text = st.text_area("Enter text to translate:", height=200, placeholder="Type something here...")

with col2:
    st.subheader("Output")
    target_languages = {
        "English": "en",
        "French": "fr",
        "German": "de",
        "Spanish": "es",
        "Chinese": "zh",
        "Hindi": "hi",
        "Arabic": "ar",
        "Russian": "ru",
        "Japanese": "ja",
        "Portuguese": "pt"
    }
    
    selected_lang_name = st.selectbox("Select target language:", list(target_languages.keys()))
    target_lang_code = target_languages[selected_lang_name]
    
    translate_btn = st.button("Translate", type="primary")

if translate_btn:
    if source_text:
        with st.spinner("Translating..."):
            try:
                detected_lang = translator.detect_language(source_text)
                translation = translator.translate(source_text, target_lang=target_lang_code)            
                st.success("Translation Complete!")
                st.info(f"Detected Source Language: **{detected_lang}**")
                st.text_area("Translated Text:", value=translation, height=200)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some text to translate.")


import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, M2M100ForConditionalGeneration, M2M100Tokenizer
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

class SmartTranslator:
    def __init__(self):
        print("Loading models... This might take a minute.")
        
        # Load Language Detection Model
        # papluca/xlm-roberta-base-language-detection supports 20 languages
        self.detect_model_name = "papluca/xlm-roberta-base-language-detection"
        self.detect_tokenizer = AutoTokenizer.from_pretrained(self.detect_model_name)
        self.detect_model = AutoModelForSequenceClassification.from_pretrained(self.detect_model_name)
        
        # Load Translation Model
        # facebook/m2m100_418M is a multilingual translation model
        self.trans_model_name = "facebook/m2m100_418M"
        self.trans_tokenizer = M2M100Tokenizer.from_pretrained(self.trans_model_name)
        self.trans_model = M2M100ForConditionalGeneration.from_pretrained(self.trans_model_name)
        
        # Mapping from XLM-R lang codes to M2M100 lang codes if they differ
        # M2M100 uses specific codes like 'en', 'fr', 'de', 'zh' etc.
        # papluca model outputs: 'ar', 'bg', 'de', 'el', 'en', 'es', 'fr', 'hi', 'it', 'ja', 'nl', 'pl', 'pt', 'ru', 'sw', 'th', 'tr', 'ur', 'vi', 'zh'
        # These mostly match, but we need to ensure M2M100 supports them.
        self.lang_map = {
            'zh-cn': 'zh', # Example if detection output is specific
            'zh-tw': 'zh',
        }

    def detect_language(self, text):
        inputs = self.detect_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            logits = self.detect_model(**inputs).logits
        
        predicted_class_id = logits.argmax().item()
        detected_lang = self.detect_model.config.id2label[predicted_class_id]
        
        # Normalize if needed
        detected_lang = self.lang_map.get(detected_lang, detected_lang)
        
        return detected_lang

    def translate(self, text, target_lang="en"):
        src_lang = self.detect_language(text)
        print(f"Detected language: {src_lang}")
        
        if src_lang == target_lang:
            return text
            
        # Set source language for tokenizer
        # M2M100 requires setting the src_lang
        try:
            self.trans_tokenizer.src_lang = src_lang
        except KeyError:
            print(f"Warning: Language '{src_lang}' might not be supported by the translation model directly. Defaulting to 'en' or trying anyway.")
            # If not supported, we might fail or need a fallback. M2M100 supports many, but let's see.

        encoded_input = self.trans_tokenizer(text, return_tensors="pt")
        
        # Generate translation
        generated_tokens = self.trans_model.generate(
            **encoded_input, 
            forced_bos_token_id=self.trans_tokenizer.get_lang_id(target_lang)
        )
        
        translated_text = self.trans_tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        return translated_text

if __name__ == "__main__":
    translator = SmartTranslator()
    
    print("\n--- Smart AI Translator ---")
    print("Type 'quit' to exit.")
    
    while True:
        user_input = input("\nEnter text to translate (to English): ")
        if user_input.lower() in ['quit', 'exit']:
            break
            
        if not user_input.strip():
            continue
            
        try:
            result = translator.translate(user_input)
            print(f"Translation: {result}")
        except Exception as e:
            print(f"Error during translation: {e}")

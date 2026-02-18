from main import SmartTranslator

def test_translator():
    translator = SmartTranslator()
    
    test_cases = [
        ("Bonjour le monde", "fr", "en"),
        ("Hola mundo", "es", "en"),
        ("Guten Tag", "de", "en"),
        ("Hello world", "en", "fr") # Test converting English to French
    ]
    
    print("\n--- Starting Verification ---")
    
    for text, expected_src, target_lang in test_cases:
        print(f"\nTesting: '{text}'")
        detected_lang = translator.detect_language(text)
        print(f"Detected: {detected_lang} (Expected: {expected_src})")
        
        translation = translator.translate(text, target_lang=target_lang)
        print(f"Translation to {target_lang}: {translation}")
        
    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    test_translator()

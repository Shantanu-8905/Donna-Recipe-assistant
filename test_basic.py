"""
Minimal test to verify basic functionality
"""
import sys

def test_imports():
    """Test if all modules can be imported"""
    print("Testing module imports...\n")
    
    modules = [
        ('advanced_data_processor', 'AdvancedDataProcessor'),
        ('nlp_engine', 'NLPEngine'),
        ('context_manager', 'ConversationContext'),
    ]
    
    success = True
    
    for module_name, class_name in modules:
        try:
            module = __import__(module_name)
            cls = getattr(module, class_name)
            print(f"✅ {module_name}.{class_name}")
        except Exception as e:
            print(f"❌ {module_name}.{class_name} - Error: {e}")
            success = False
    
    return success

def test_speech():
    """Test speech handler"""
    print("\nTesting speech handler...\n")
    
    try:
        from advanced_speech_handler import AdvancedSpeechHandler
        
        # Test without Whisper first (faster)
        sh = AdvancedSpeechHandler(use_whisper=False)
        print("✅ Speech handler initialized")
        
        # Test TTS
        sh.speak("Testing text to speech", rate=150)
        print("✅ Text-to-speech working")
        
        return True
    except Exception as e:
        print(f"❌ Speech handler error: {e}")
        return False

def test_nlp():
    """Test NLP engine"""
    print("\nTesting NLP engine...\n")
    
    try:
        from nlp_engine import NLPEngine
        
        nlp = NLPEngine()
        print("✅ NLP engine initialized")
        
        # Test keyword extraction
        test_input = "I would like vegetarian"
        options = ['vegetarian', 'non-vegetarian']
        
        match, score = nlp.fuzzy_match(test_input, options)
        
        if match == 'vegetarian':
            print(f"✅ Keyword extraction working (matched: {match}, score: {score})")
            return True
        else:
            print(f"⚠️ Keyword extraction issue (matched: {match}, expected: vegetarian)")
            return False
            
    except Exception as e:
        print(f"❌ NLP engine error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data():
    """Test data processor"""
    print("\nTesting data processor...\n")
    
    try:
        from advanced_data_processor import AdvancedDataProcessor
        import os
        
        if not os.path.exists('indian_recipes.csv'):
            print("❌ Dataset file 'indian_recipes.csv' not found")
            return False
        
        dp = AdvancedDataProcessor('indian_recipes.csv')
        df = dp.clean_and_enhance_data()
        
        print(f"✅ Data processor working ({len(df)} recipes loaded)")
        return True
        
    except Exception as e:
        print(f"❌ Data processor error: {e}")
        return False

def main():
    print("=" * 70)
    print(" Dauna AI - Basic Functionality Test")
    print("=" * 70)
    print()
    
    tests = [
        ("Module Imports", test_imports),
        ("Data Processing", test_data),
        ("NLP Engine", test_nlp),
        ("Speech Handler", test_speech),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'=' * 70}")
        print(f" {test_name}")
        print('=' * 70)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print(" Test Summary")
    print("=" * 70)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:.<50} {status}")
    
    print("=" * 70)
    
    if all(result for _, result in results):
        print("\n✅ All tests passed! You can run: python main_enhanced.py")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("1. Ensure 'indian_recipes.csv' is in the current directory")
        print("2. Install dependencies: pip install -r requirements_enhanced.txt")
        print("3. Download spaCy model: python -m spacy download en_core_web_sm")
        print("4. Check your microphone is connected and working")

if __name__ == "__main__":
    main()
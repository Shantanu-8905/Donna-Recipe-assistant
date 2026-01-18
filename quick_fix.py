"""
Quick diagnostic and fix script
"""
import sys

def check_dependencies():
    print("Checking dependencies...")
    
    required = [
        'pandas',
        'numpy',
        'transformers',
        'sentence_transformers',
        'torch',
        'spacy',
        'rapidfuzz',
        'speech_recognition',
        'pyttsx3'
    ]
    
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️ Missing packages: {', '.join(missing)}")
        print(f"\nInstall with: pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All dependencies installed!")
    return True

def check_spacy_model():
    print("\nChecking spaCy model...")
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("  ✅ spaCy model loaded")
        return True
    except:
        print("  ❌ spaCy model not found")
        print("\nInstall with: python -m spacy download en_core_web_sm")
        return False

def check_dataset():
    print("\nChecking dataset...")
    import os
    if os.path.exists('indian_recipes.csv'):
        print("  ✅ Dataset found")
        return True
    else:
        print("  ❌ Dataset not found")
        print("\nPlease ensure 'indian_recipes.csv' is in the current directory")
        return False

def main():
    print("=" * 70)
    print("Dauna AI - Quick Diagnostic")
    print("=" * 70)
    print()
    
    checks = [
        check_dependencies(),
        check_spacy_model(),
        check_dataset()
    ]
    
    print("\n" + "=" * 70)
    if all(checks):
        print("✅ All checks passed! You're ready to run Dauna AI.")
        print("\nRun with: python main_enhanced.py")
    else:
        print("⚠️ Some checks failed. Please fix the issues above.")
    print("=" * 70)

if __name__ == "__main__":
    main()
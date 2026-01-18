import sys
import os
import warnings
warnings.filterwarnings('ignore')

from advanced_data_processor import AdvancedDataProcessor
from advanced_speech_handler import AdvancedSpeechHandler
from nlp_engine import NLPEngine
from context_manager import ConversationContext
from enhanced_conversation_manager import EnhancedConversationManager
import pandas as pd

def check_dependencies():
    """Check if all required files are present"""
    print("🔍 Checking dependencies...")
    
    required_files = [
        'indian_recipes.csv',
        'advanced_data_processor.py',
        'advanced_speech_handler.py',
        'nlp_engine.py',
        'context_manager.py',
        'enhanced_conversation_manager.py'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"❌ Missing files: {', '.join(missing)}")
        return False
    
    print("✅ All dependencies found\n")
    return True

def initialize_system():
    """Set up all system components"""
    print("=" * 70)
    print(" 🍛 DONNA AI - Intelligent Recipe Discovery System 🍛")
    print("=" * 70)
    print("\n🔧 Initializing system components...\n")
    
    # Load the recipe data
    print("📊 Loading and processing recipe dataset...")
    try:
        dp = AdvancedDataProcessor('indian_recipes.csv')
        df_cleaned = dp.clean_and_enhance_data()
        
        # Make sure we got data back
        if df_cleaned is None or len(df_cleaned) == 0:
            raise ValueError("No data loaded from processor")
        
        print(f"✅ Loaded {len(df_cleaned)} recipes")
        print(f"   • Columns: {len(df_cleaned.columns)}")
        print(f"   • Missing values: {df_cleaned.isnull().sum().sum()}")
        
        # Show what we're working with
        print(f"\n   📋 Data Summary:")
        print(f"   • Diets: {df_cleaned['diet'].nunique()} ({', '.join(df_cleaned['diet'].unique())})")
        print(f"   • Courses: {', '.join(df_cleaned['course'].unique())}")
        print(f"   • Regions: {df_cleaned['region'].nunique()}")
        print(f"   • Avg difficulty: {df_cleaned['difficulty'].mean():.1f}/10")
        
    except FileNotFoundError:
        print("❌ Error: 'indian_recipes.csv' not found!")
        print("   Place the dataset file in the current directory.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Generate embeddings for semantic search
    print("\n🧠 Creating semantic embeddings (this may take a moment)...")
    try:
        # See if we already have them
        if os.path.exists('recipe_embeddings.pkl'):
            print("   📦 Found existing embeddings, loading...")
            import pickle
            with open('recipe_embeddings.pkl', 'rb') as f:
                dp.embeddings = pickle.load(f)
            print("✅ Embeddings loaded")
        else:
            dp.create_embeddings()
            print("✅ Embeddings created and saved")
    except Exception as e:
        print(f"⚠️  Warning: Could not create embeddings: {e}")
        print("   Continuing without semantic search features...")
    
    # Initialize database
    print("\n💾 Setting up database...")
    try:
        dp.setup_database()
        print("✅ Database ready")
    except Exception as e:
        print(f"⚠️  Warning: Database setup issue: {e}")
        print("   Continuing with limited persistence...")
    
    # Load NLP models
    print("\n🤖 Loading NLP models...")
    try:
        nlp = NLPEngine()
        print("✅ NLP engine ready")
    except Exception as e:
        print(f"❌ Error initializing NLP: {e}")
        print("   Please install spacy models: python -m spacy download en_core_web_sm")
        sys.exit(1)
    
    # Set up speech recognition
    print("\n🎤 Initializing speech systems...")
    sh = None
    try:
        # Try Whisper first - it's better
        sh = AdvancedSpeechHandler(use_whisper=True)
        print("✅ Speech handler ready (Whisper ASR)")
    except Exception as e:
        print(f"   ⚠️  Whisper not available: {e}")
        print("   Trying fallback speech recognition...")
        try:
            sh = AdvancedSpeechHandler(use_whisper=False)
            print("✅ Speech handler ready (Google ASR)")
        except Exception as e:
            print(f"❌ Error initializing speech: {e}")
            print("   Check microphone connection and audio settings.")
            sys.exit(1)
    
    # Setup context for the conversation
    print("\n💭 Setting up conversation context...")
    try:
        context = ConversationContext()
        print("✅ Context manager ready")
    except Exception as e:
        print(f"⚠️  Warning: Context manager issue: {e}")
        print("   Continuing without session persistence...")
        context = ConversationContext()
    
    # Create the main conversation manager
    print("\n🎯 Initializing conversation manager...")
    try:
        cm = EnhancedConversationManager(dp, sh, nlp, context)
        print("✅ System fully initialized!\n")
    except Exception as e:
        print(f"❌ Error creating conversation manager: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    return cm

def display_startup_info():
    """Show instructions and welcome message"""
    print("=" * 70)
    print(" 📖 Ready to discover delicious Indian recipes!")
    print(" You can say things like:")
    print("   • 'Show me sweet vegetarian desserts'")
    print("   • 'Find quick recipes from North India'")
    print("   • 'I want something spicy'")
    print(" Press Ctrl+C to exit anytime.")
    print("=" * 70)
    print()

def main():
    """Main application entry point"""
    try:
        # Check that everything we need is there
        if not check_dependencies():
            print("Please ensure all required files are present.")
            sys.exit(1)
        
        # Start up all the components
        cm = initialize_system()
        
        # Show the welcome screen
        display_startup_info()
        
        # Greet user
        print("Welcome! Starting recipe assistant...")
        
        # Main conversation loop
        session_count = 0
        max_sessions = 10
        
        while session_count < max_sessions:
            try:
                session_count += 1
                print(f"\n{'='*70}")
                print(f"📍 Conversation Session {session_count}")
                print(f"{'='*70}\n")
                
                # Start the conversation
                cm.run_enhanced_conversation()
                
                # See if they want to go again
                print("\n" + "-" * 70)
                try:
                    cm.sh.speak("Would you like to search for another recipe?")
                    response, _ = cm.sh.listen(timeout=8)
                    
                    if not response:
                        print("No response detected. Ending session.")
                        break
                    
                    # Look for yes/no
                    positive_words = ['yes', 'yeah', 'sure', 'another', 'more', 'again', 'yep', 'ok']
                    if not any(word in response.lower() for word in positive_words):
                        print("Looks like they're done.")
                        break
                    
                    # Clear context for next search
                    cm.context.reset_session()
                    print("\n🔄 Starting new search session...\n")
                    
                except Exception as e:
                    print(f"Could not process response: {e}")
                    break
                
            except KeyboardInterrupt:
                raise  # Re-raise to outer handler
                
            except Exception as e:
                print(f"\n⚠️  Something went wrong: {e}")
                import traceback
                traceback.print_exc()
                
                # Ask if they want to try again
                try:
                    cm.sh.speak("I encountered an issue. Would you like to try again?")
                    response, _ = cm.sh.listen(timeout=6)
                    
                    retry_words = ['yes', 'yeah', 'sure', 'retry', 'again', 'ok']
                    if response and any(word in response.lower() for word in retry_words):
                        cm.context.reset_session()
                        print("🔄 Retrying...\n")
                        continue
                    else:
                        break
                except:
                    print("Unable to continue. Exiting...")
                    break
        
        # Say goodbye
        print("\n" + "=" * 70)
        try:
            cm.sh.speak("Thanks for using Donna!")
        except:
            pass
        print(" Thank you for using Donna!")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        print("=" * 70)
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n" + "=" * 70)
        print("🔧 TROUBLESHOOTING:")
        print("=" * 70)
        print("1. Verify dataset: Check if 'indian_recipes.csv' exists")
        print("2. Clean dataset: Run 'python data_cleaner.py'")
        print("3. Install dependencies: pip install -r requirements_enhanced.txt")
        print("4. Check logs: Look in the 'logs' directory for details")
        print("5. Run diagnostic: python quick_fix.py")
        print("=" * 70)
        
        sys.exit(1)

if __name__ == "__main__":
    main()

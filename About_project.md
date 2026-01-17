# About Donna AI - Technical Documentation

## Project Overview

**Donna AI** is an intelligent recipe discovery system that uses natural language processing, speech recognition, and machine learning to help users find Indian recipes through conversational interaction.

## What It Does

### Core Functionality

1. **Voice-Enabled Conversation**
   - Listens to user requests via microphone
   - Processes natural language queries
   - Responds with recipes via text-to-speech

2. **Smart Recipe Filtering**
   - Multi-criteria filtering engine
   - Semantic understanding of recipes
   - Intelligent matching of user preferences

3. **Personalization**
   - User profile persistence
   - Preference learning
   - Interaction history tracking

4. **Data Intelligence**
   - 255 cleaned Indian recipes
   - Semantic embeddings for similarity search
   - Advanced fuzzy matching

## Technology Stack

### Core Language
- **Python 3.11** - Main programming language
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing

### Machine Learning & NLP
- **spaCy** - Natural language processing
  - Named entity recognition
  - Text tokenization
  - Lemmatization

- **Sentence-Transformers** - Semantic embeddings
  - Model: `all-MiniLM-L6-v2`
  - Purpose: Recipe similarity search
  - Optimized for semantic meaning

- **Transformers** - Deep learning models
  - Zero-shot classification
  - Intent detection
  - Sentiment analysis

- **scikit-learn** - Machine learning utilities
  - TF-IDF vectorization
  - Cosine similarity
  - Feature engineering

- **TensorFlow** - Deep learning framework
  - Inference engine
  - Model optimization

### Speech Processing
- **Faster-Whisper** - Speech recognition
  - Model: Base (optimized for CPU)
  - Language: English
  - Compute: int8 (quantized)

- **pyttsx3** - Text-to-speech engine
  - Offline TTS (no internet required)
  - Supports multiple voices
  - Configurable speech rate/volume

- **SpeechRecognition** - Google ASR fallback
  - Web API integration
  - Confidence scoring

- **librosa** - Audio processing
  - Audio feature extraction
  - Resampling

- **noisereduce** - Audio enhancement
  - Noise suppression
  - Audio quality improvement

### Data Management
- **SQLite** - Lightweight database
  - Recipe storage
  - User profiles
  - Interaction logs

- **Pickle** - Python object serialization
  - Embedding cache
  - Model persistence

- **CSV** - Data format for recipes
  - Clean dataset: `indian_recipes_cleaned.csv`

### Development Tools
- **rapidfuzz** - Fuzzy string matching
  - State name matching
  - Levenshtein distance
  - Multiple scoring algorithms

- **logging** - Application logging
  - Debug information
  - Error tracking
  - Performance metrics

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────┐
│          User Interface (Voice/Text)               │
│  (AdvancedSpeechHandler)                           │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│        Conversation Manager                        │
│  (EnhancedConversationManager)                     │
│  - Dialog flow                                     │
│  - User intent routing                             │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┼──────────┬───────────┐
        │          │          │           │
┌───────▼──┐  ┌───▼──────┐ ┌─▼──────┐ ┌─▼────────┐
│   NLP    │  │  Context │ │ Data   │ │ Speech   │
│  Engine  │  │ Manager  │ │Handler │ │ Handler  │
└──────────┘  └──────────┘ └────────┘ └──────────┘
        │                        │
        └────────┬───────────────┘
                 │
        ┌────────▼────────┐
        │   SQLite DB     │
        │   Embeddings    │
        │   User Profiles │
        └─────────────────┘
```

### Data Flow

1. **Input Phase**
   - User speaks or types query
   - Speech → Text conversion (if voice)
   - Audio preprocessing (noise reduction)

2. **Processing Phase**
   - NLP parsing (keyword extraction)
   - Intent classification
   - Context analysis
   - Sentiment detection

3. **Filtering Phase**
   - Apply user constraints
   - Database query execution
   - Semantic similarity ranking
   - Result filtering

4. **Output Phase**
   - Format recommendations
   - Generate response text
   - Text → Speech conversion
   - Log interaction

## Key Features Explained

### Natural Language Processing

**Keyword Extraction:**
- Extracts diet, course, region from user input
- Handles variations (hyphen vs space)
- Negation detection ("non-vegetarian")
- Word boundary matching

**Intent Recognition:**
- Determines user goal from text
- 13 predefined intents
- Zero-shot classification
- Confidence scoring

**Sentiment Analysis:**
- Analyzes user emotions
- Adjusts response tone
- Tracks user satisfaction

### Recipe Database

**Cleaned Data (255 recipes):**
- ✅ No missing values
- ✅ Standardized formats
- ✅ Derived features calculated
- ✅ Indexed for performance

**Features per Recipe:**
- Name, ingredients, diet, course
- State, region, flavor profile
- Prep time, cook time, difficulty
- Total time, ingredient count
- Ingredient list (parsed)
- Search text (indexable)

### Semantic Search

**Embedding Generation:**
- Uses `sentence-transformers`
- Encodes: recipe name + ingredients + flavor
- Cached in `recipe_embeddings.pkl`
- Fast similarity computation via cosine distance

**Similarity Matching:**
- Finds recipes similar to query
- Returns ranked results
- Confidence scores
- Handles semantic meaning

### Filtering Engine

**Multi-Criteria Filtering:**
- Diet (vegetarian/non-vegetarian)
- Course (main, dessert, snack, starter)
- Region/State (fuzzy matched)
- Time constraints (prep, cook, total)
- Difficulty level (1-10)
- Ingredients (include/exclude)
- Flavor profile (spicy, mild, sweet, etc.)

**Performance:**
- Indexed database queries
- In-memory filtering
- Lazy loading of results

## File Structure Explained

### Core Modules

**main_enhanced.py**
- Application entry point
- System initialization
- Component setup
- Error handling
- Multi-session loop

**advanced_data_processor.py**
- Recipe data loading
- Dataset cleaning detection
- Embedding creation
- Database setup
- Filtering logic
- Similarity search

**nlp_engine.py**
- Keyword extraction
- Intent classification
- Sentiment analysis
- Entity recognition
- Synonym matching

**enhanced_conversation_manager.py**
- Dialog management
- User input handling
- Response generation
- Conversation flow
- Preference tracking

**advanced_speech_handler.py**
- Whisper speech recognition
- Google ASR fallback
- Text-to-speech output
- Audio preprocessing
- Confidence handling

**context_manager.py**
- Session state tracking
- User profile management
- Conversation history
- Preference persistence
- Database integration

**data_cleaner.py**
- Dataset validation
- Missing value handling
- Text standardization
- Feature engineering
- Data quality reporting

**logger_config.py**
- Logging setup
- File/console output
- Session tracking
- Error logging

### Data Files

**indian_recipes_cleaned.csv**
- 255 recipes (cleaned)
- 16 columns (features)
- UTF-8 encoding
- Tab/comma separated

**recipes.db**
- SQLite database
- Created on first run
- User profiles table
- Interactions table
- Indexed for speed

**recipe_embeddings.pkl**
- Serialized embeddings
- 255 vectors × 384 dimensions
- Binary pickle format
- Cached for performance

**vosk-model-small-en-us-0.15/**
- Vosk speech recognition model
- Offline ASR engine
- ~50MB size
- English US language

## Dependencies

### Required Packages
```
pandas>=1.3.0
numpy>=1.21.0
scikit-learn>=1.0.0
sentence-transformers>=2.2.0
torch>=1.10.0
transformers>=4.20.0
spacy>=3.3.0
faster-whisper>=0.7.0
pyttsx3>=2.90
speech-recognition>=3.10.0
librosa>=0.10.0
noisereduce>=2.0.0
soundfile>=0.10.3
rapidfuzz>=2.13.0
```

### Python Requirements
- Python 3.11+
- pip (package manager)
- Virtual environment (recommended)

## Performance Characteristics

### Speed Metrics
- Cold startup: 5-8 seconds
- Warm startup: 2-3 seconds
- Database query: <100ms
- Embedding generation: 50-100ms per recipe
- Semantic search: 500ms-1s
- Speech recognition: 2-5 seconds (audio dependent)

### Resource Usage
- Memory: ~500MB (models loaded)
- CPU: 40-60% during processing
- Disk: ~2GB (including models)
- Network: Optional (Google ASR fallback)

## Recent Bug Fixes

### Non-Vegetarian Selection Bug (Fixed)
**Issue:** Saying "non-vegetarian" selected vegetarian recipes
**Root Cause:** Substring matching found "vegetarian" inside "non-vegetarian"
**Solution:** Implemented word boundary matching with negation detection

**Key Changes:**
- Sort options by length (longest first)
- Use regex word boundaries: `\bword\b`
- Normalize hyphens to spaces
- Detect negation prefixes ("non-", "de-")

## Future Enhancements

- [ ] Multi-language support
- [ ] User recipe ratings
- [ ] Shopping list generation
- [ ] Dietary restriction profiles
- [ ] Cooking tutorial videos
- [ ] Ingredient substitution suggestions
- [ ] Nutritional information
- [ ] Recipe sharing features

## Quality Assurance

### Testing Suite
- Integration tests (`test_integration.py`)
- NLP tests (`test_keyword_extraction.py`)
- Diet filter tests (`test_diet_filter.py`)
- Filter validation (`test_all_filters.py`)

### Code Quality
- Type hints throughout
- Docstrings on all functions
- Error handling with try-catch
- Logging for debugging
- Syntax validation with py_compile

## Security Considerations

- User data stored locally (SQLite)
- No external data transmission
- API calls minimized (fallback only)
- Input validation on all user queries
- SQL injection prevention (parameterized queries)

## Deployment

### System Requirements
- Windows/Linux/Mac
- Python 3.11+
- 4GB RAM minimum
- 2GB disk space
- Microphone (for voice features)
- Speaker (for audio output)

### Environment Setup
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements_enhanced.txt
python -m spacy download en_core_web_sm
python main_enhanced.py
```

## Monitoring & Debugging

### Log Files
- Location: `logs/` directory
- Format: `donna_YYYYMMDD_HHMMSS.log`
- Contains: Timestamps, log levels, messages

### Debug Commands
```bash
# Syntax check
python -m py_compile nlp_engine.py

# System diagnostics
python system_status.py

# Quick fixes
python quick_fix.py
```

---

**Last Updated:** January 17, 2026
**Version:** 1.0
**Status:** Production Ready

# 🍛 Donna AI - Intelligent Indian Recipe Discovery

A voice-enabled AI assistant that helps you discover, filter, and explore Indian recipes through natural conversation.

## Quick Start

### Installation

1. **Clone and navigate to project:**
```bash
cd "c:\DRIVE\Projects\Dauna 2.0"
```

2. **Install dependencies:**
```bash
pip install -r requirements_enhanced.txt
```

3. **Download NLP models:**
```bash
python -m spacy download en_core_web_sm
```

4. **Run the application:**
```bash
python main_enhanced.py
```

## How to Use

### Starting a Conversation

When you run the app, it will greet you and guide you through 5 conversation steps:

1. **Greeting** - Donna welcomes you
2. **Diet Selection** - Choose vegetarian or non-vegetarian
3. **Restrictions** - Add any ingredient preferences
4. **Course Selection** - Pick what you want (snack, main, dessert, etc.)
5. **Recipe Discovery** - Get personalized recommendations

### Example Conversations

**User:** "I want a vegetarian main course"
**Donna:** Shows vegetarian main course recipes

**User:** "Find me something with paneer, not too spicy"
**Donna:** Filters for paneer recipes with lower spice levels

**User:** "Quick snacks under 30 minutes"
**Donna:** Shows snacks that take less than 30 minutes

## Dataset

The system uses a cleaned dataset of **255 Indian recipes** including:
- **Diets:** Vegetarian (226) | Non-vegetarian (29)
- **Courses:** Main, Dessert, Snack, Starter
- **Regions:** North, South, East, West India
- **Features:** Prep time, cook time, difficulty, ingredients, flavor profile

### Data Quality

- ✅ All invalid entries cleaned
- ✅ Zero missing values
- ✅ Standardized formats
- ✅ 16 engineered features per recipe

## Features

### 🎤 Voice Interface
- **Speech Recognition:** Listens to your spoken requests
- **Text-to-Speech:** Responds with natural audio
- **Automatic ASR Fallback:** Switches between Whisper and Google ASR

### 🧠 Smart Filtering
- Filter by diet (veg/non-veg)
- Filter by course type
- Filter by region/state
- Filter by cooking time
- Filter by difficulty level
- Include/exclude ingredients
- Filter by flavor profile

### 🔍 Semantic Search
- Understand meaning, not just keywords
- Find similar recipes
- Natural language understanding
- Confidence-based matching

### 💾 Data Management
- Persistent user profiles
- Recipe interaction history
- SQLite database for fast queries
- Pickle-based embeddings cache

## Project Structure

```
Dauna 2.0/
├── main_enhanced.py                 # Entry point
├── advanced_data_processor.py        # Data filtering & search
├── advanced_speech_handler.py        # Speech I/O
├── nlp_engine.py                     # Natural language processing
├── enhanced_conversation_manager.py  # Dialog flow
├── context_manager.py                # Session state
├── data_cleaner.py                   # Dataset cleaning
├── logger_config.py                  # Logging setup
├── indian_recipes_cleaned.csv        # Clean recipe dataset
├── requirements_enhanced.txt         # Dependencies
├── logs/                            # Application logs
└── vosk-model-small-en-us-0.15/     # Speech recognition model
```

## Commands & Examples

### Run the System
```bash
python main_enhanced.py
```

### Clean Dataset (if needed)
```bash
python data_cleaner.py
```

### Check System Status
```bash
python system_status.py
```

### Run Tests
```bash
python test_integration.py      # Integration test
python test_keyword_extraction.py  # NLP test
python verify_fix.py            # Verify diet filtering
```

## Troubleshooting

### Issue: "indian_recipes.csv not found"
**Solution:** Ensure the CSV file is in the project directory

### Issue: Speech recognition not working
**Solution:** Check microphone is connected and not muted

### Issue: Whisper model failing to load
**Solution:** Install with: `pip install faster-whisper`

### Issue: Spacy model missing
**Solution:** Run: `python -m spacy download en_core_web_sm`

## Known Limitations

- Abbreviations like "veg" and "non-veg" may not match (use full words)
- Requires active internet for some ASR fallbacks
- Microphone input required for voice features
- Works best with clear English speech

## Recent Updates

### Version 1.0 (Latest)
- ✅ Fixed non-vegetarian selection bug
- ✅ Improved NLP keyword extraction
- ✅ Cleaned dataset with 0% missing values
- ✅ Enhanced multi-session support
- ✅ Better error handling and logging

## Performance

- **Startup Time:** ~5-8 seconds
- **Recipe Filter:** <100ms
- **Semantic Search:** ~500ms-1s
- **Speech Recognition:** 2-5 seconds (depends on audio length)
- **Memory Usage:** ~500MB (with models loaded)

## Support

For issues or questions:
1. Check the logs in the `logs/` directory
2. Review the About_project.md for technical details
3. Run diagnostic: `python quick_fix.py`


**Built with:** Python 3.11 | TensorFlow | Transformers | spaCy | Whisper | pyttsx3

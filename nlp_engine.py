# from transformers import pipeline
# from textblob import TextBlob
# import re
# from typing import Dict, List, Tuple
# from rapidfuzz import process, fuzz
# from typing import Optional, Tuple
# import spacy

# class NLPEngine:
#     def __init__(self):
#         # Load spaCy model for NER
#         try:
#             self.nlp = spacy.load("en_core_web_sm")
#         except:
#             print("Downloading spaCy model...")
#             import os
#             os.system("python -m spacy download en_core_web_sm")
#             self.nlp = spacy.load("en_core_web_sm")
        
#         # Intent classifier using zero-shot classification
#         self.intent_classifier = pipeline(
#             "zero-shot-classification",
#             model="facebook/bart-large-mnli"
#         )
        
#         # Sentiment analyzer
#         self.sentiment_analyzer = pipeline(
#             "sentiment-analysis",
#             model="distilbert-base-uncased-finetuned-sst-2-english"
#         )
        
#         # Define intents
#         self.intents = [
#             "search_recipe",
#             "filter_by_diet",
#             "filter_by_course",
#             "filter_by_region",
#             "get_recipe_details",
#             "find_similar",
#             "suggest_alternative",
#             "express_preference",
#             "ask_cooking_time",
#             "ask_ingredients",
#             "express_confusion",
#             "confirm_selection",
#             "end_conversation"
#         ]
    
#     def analyze_intent(self, text: str, threshold: float = 0.5) -> Tuple[str, float]:
#         """Classify user intent with confidence score"""
#         result = self.intent_classifier(text, self.intents)
        
#         intent = result['labels'][0]
#         confidence = result['scores'][0]
        
#         if confidence < threshold:
#             return "unclear", confidence
        
#         return intent, confidence
    
#     def extract_entities(self, text: str) -> Dict[str, List[str]]:
#         """Extract named entities from text"""
#         doc = self.nlp(text)
        
#         entities = {
#             'food': [],
#             'location': [],
#             'time': [],
#             'quantity': []
#         }
        
#         for ent in doc.ents:
#             if ent.label_ in ['GPE', 'LOC']:  # Location
#                 entities['location'].append(ent.text)
#             elif ent.label_ in ['TIME', 'DATE']:
#                 entities['time'].append(ent.text)
#             elif ent.label_ in ['QUANTITY', 'CARDINAL']:
#                 entities['quantity'].append(ent.text)
        
#         # Extract food items (custom logic)
#         food_keywords = ['chicken', 'paneer', 'rice', 'dal', 'curry', 
#                         'vegetables', 'fish', 'mutton', 'egg']
        
#         for token in doc:
#             if token.text.lower() in food_keywords:
#                 entities['food'].append(token.text.lower())
        
#         return entities
    
#     def analyze_sentiment(self, text: str) -> Dict[str, float]:
#         """Analyze sentiment of user response"""
#         result = self.sentiment_analyzer(text)[0]
        
#         return {
#             'label': result['label'],
#             'score': result['score'],
#             'is_positive': result['label'] == 'POSITIVE'
#         }
    
#     def fuzzy_match(self, 
#                    user_input: str, 
#                    valid_options: List[str], 
#                    threshold: int = 70) -> Tuple[Optional[str], int]:
#         """Fuzzy match user input with valid options"""
#         if not user_input:
#             return None, 0
        
#         # Try multiple fuzzy matching strategies
#         match1, score1 = process.extractOne(
#             user_input, valid_options, scorer=fuzz.ratio
#         )
        
#         match2, score2 = process.extractOne(
#             user_input, valid_options, scorer=fuzz.partial_ratio
#         )
        
#         match3, score3 = process.extractOne(
#             user_input, valid_options, scorer=fuzz.token_sort_ratio
#         )
        
#         # Take the best match
#         best_match = max(
#             [(match1, score1), (match2, score2), (match3, score3)],
#             key=lambda x: x[1]
#         )
        
#         if best_match[1] >= threshold:
#             return best_match
        
#         return None, best_match[1]
    
#     def extract_dietary_restrictions(self, text: str) -> List[str]:
#         """Extract dietary restrictions from text"""
#         restrictions = []
        
#         restriction_keywords = {
#             'vegan': ['vegan'],
#             'gluten-free': ['gluten free', 'gluten-free', 'celiac'],
#             'dairy-free': ['dairy free', 'dairy-free', 'lactose'],
#             'nut-free': ['nut free', 'nut-free', 'no nuts', 'allergy'],
#             'low-carb': ['low carb', 'keto', 'atkins'],
#             'spicy': ['spicy', 'hot', 'chili'],
#             'non-spicy': ['not spicy', 'mild', 'no spice']
#         }
        
#         text_lower = text.lower()
        
#         for restriction, keywords in restriction_keywords.items():
#             if any(keyword in text_lower for keyword in keywords):
#                 restrictions.append(restriction)
        
#         return restrictions















































import spacy
from transformers import pipeline
from textblob import TextBlob
import re
from typing import Dict, List, Tuple, Optional
from rapidfuzz import process, fuzz

class NLPEngine:
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("Downloading spaCy model...")
            import os
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        # Intent classifier
        try:
            self.intent_classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli"
            )
        except:
            print("Could not load intent classifier")
            self.intent_classifier = None
        
        # Sentiment analysis
        try:
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
        except:
            print("Could not load sentiment analyzer")
            self.sentiment_analyzer = None
        
        # Define intents
        self.intents = [
            "search_recipe",
            "filter_by_diet",
            "filter_by_course",
            "filter_by_region",
            "get_recipe_details",
            "find_similar",
            "suggest_alternative",
            "express_preference",
            "ask_cooking_time",
            "ask_ingredients",
            "express_confusion",
            "confirm_selection",
            "end_conversation"
        ]
    
    def extract_keywords(self, text: str, valid_options: List[str]) -> List[Tuple[str, float]]:
        """
        Extract keywords from text that match valid options
        Returns list of (keyword, confidence) tuples
        """
        import re
        text_lower = text.lower()
        # Normalize text
        text_normalized = text_lower.replace('-', ' ')
        
        matches = []
        
        # Sort options by length (longer first)
        sorted_options = sorted(valid_options, key=lambda x: len(x.lower()), reverse=True)
        matched_options = set()
        
        for option in sorted_options:
            option_lower = option.lower()
            option_normalized = option_lower.replace('-', ' ')
            option_words = option_normalized.split()
            
            # Skip if already matched
            if any(matched.lower().find(option_lower) != -1 for matched in matched_options):
                continue
            
            # Check for exact phrase match
            if option_normalized in text_normalized:
                # Verify word boundaries
                pattern = r'\b' + r'\s+'.join(re.escape(w) for w in option_words) + r'\b'
                if re.search(pattern, text_normalized):
                    matches.append((option, 1.0))
                    matched_options.add(option)
                    continue
            
            # Check original text too
            if option_lower in text_lower:
                pattern = r'\b' + re.escape(option_lower) + r'\b'
                if re.search(pattern, text_lower):
                    matches.append((option, 1.0))
                    matched_options.add(option)
                    continue
            
            # Check for word boundary matches
            if len(option_words) > 1:
                # Check if all words appear in text
                all_words_present = all(
                    bool(re.search(r'\b' + re.escape(word) + r'\b', text_normalized))
                    for word in option_words
                )
                if all_words_present:
                    # Check if words appear in order
                    word_positions = []
                    for word in option_words:
                        match = re.search(r'\b' + re.escape(word) + r'\b', text_normalized)
                        if match:
                            word_positions.append(match.start())
                    
                    # If positions increase, words are in order
                    if len(word_positions) == len(option_words) and word_positions == sorted(word_positions):
                        # Special check for negation
                        if option_words[0] == 'non':
                            if 'non' not in text_normalized:
                                continue
                        
                        matches.append((option, 0.95))
                        matched_options.add(option)
                        continue
            
            # For single-word options
            for word in option_words:
                if len(word) > 3:
                    if re.search(r'\b' + re.escape(word) + r'\b', text_normalized):
                        # Special check for non-vegetarian
                        if option_lower == 'non-vegetarian' or option_lower == 'non vegetarian':
                            if 'non' not in text_normalized:
                                continue
                        
                        confidence = 0.85 if len(option_words) == 1 else 0.75
                        matches.append((option, confidence))
                        matched_options.add(option)
                        break
            
            # Check for synonyms
            synonyms = self.get_synonyms(option_lower)
            for syn in synonyms:
                if re.search(r'\b' + re.escape(syn) + r'\b', text_normalized):
                    matches.append((option, 0.7))
                    matched_options.add(option)
                    break
        
        # Sort by confidence
        sorted_matches = sorted(matches, key=lambda x: x[1], reverse=True)
        return sorted_matches
    
    def get_synonyms(self, word: str) -> List[str]:
        """Get common synonyms for recipe-related terms"""
        synonym_map = {
            'vegetarian': ['veg', 'veggie', 'vegetable', 'plant-based', 'meatless'],
            'non-vegetarian': ['non-veg', 'nonveg', 'meat', 'chicken', 'fish', 'egg'],
            'main course': ['main', 'entree', 'dinner', 'lunch'],
            'snack': ['snacks', 'appetizer', 'starter', 'finger food', 'tea time'],
            'dessert': ['sweet', 'desserts', 'pudding', 'cake', 'mithai'],
        }
        
        for key, synonyms in synonym_map.items():
            if word in key or key in word:
                return synonyms
        
        return []
    
    def analyze_intent(self, text: str, threshold: float = 0.5) -> Tuple[str, float]:
        """Classify user intent with confidence score"""
        if not self.intent_classifier:
            # Fallback to keyword matching
            return self.analyze_intent_fallback(text), 0.6
        
        try:
            result = self.intent_classifier(text, self.intents)
            intent = result['labels'][0]
            confidence = result['scores'][0]
            
            if confidence < threshold:
                return "unclear", confidence
            
            return intent, confidence
        except Exception as e:
            print(f"Intent classification error: {e}")
            return self.analyze_intent_fallback(text), 0.6
    
    def analyze_intent_fallback(self, text: str) -> str:
        """Simple keyword-based intent detection"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['similar', 'like this', 'recommend']):
            return 'find_similar'
        elif any(word in text_lower for word in ['bye', 'goodbye', 'exit', 'quit', 'no thanks']):
            return 'end_conversation'
        elif any(word in text_lower for word in ['yes', 'yeah', 'sure', 'okay', 'correct']):
            return 'confirm_selection'
        else:
            return 'search_recipe'
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text"""
        doc = self.nlp(text)
        
        entities = {
            'food': [],
            'location': [],
            'time': [],
            'quantity': []
        }
        
        for ent in doc.ents:
            if ent.label_ in ['GPE', 'LOC']:  # Location
                entities['location'].append(ent.text)
            elif ent.label_ in ['TIME', 'DATE']:
                entities['time'].append(ent.text)
            elif ent.label_ in ['QUANTITY', 'CARDINAL']:
                entities['quantity'].append(ent.text)
        
        # Extract food items (custom logic)
        food_keywords = ['chicken', 'paneer', 'rice', 'dal', 'curry', 
                        'vegetables', 'fish', 'mutton', 'egg']
        
        for token in doc:
            if token.text.lower() in food_keywords:
                entities['food'].append(token.text.lower())
        
        return entities
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of user response"""
        if not self.sentiment_analyzer:
            # Fallback to TextBlob
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            return {
                'label': 'POSITIVE' if polarity > 0 else 'NEGATIVE' if polarity < 0 else 'NEUTRAL',
                'score': abs(polarity),
                'is_positive': polarity > 0
            }
        
        try:
            result = self.sentiment_analyzer(text)[0]
            return {
                'label': result['label'],
                'score': result['score'],
                'is_positive': result['label'] == 'POSITIVE'
            }
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return {'label': 'NEUTRAL', 'score': 0.5, 'is_positive': True}
    
    def fuzzy_match(self, 
                   user_input: str, 
                   valid_options: List[str], 
                   threshold: int = 70) -> Tuple[Optional[str], int]:
        """Fuzzy match user input with valid options using multiple strategies"""
        if not user_input or not valid_options:
            return None, 0
        
        # First, try keyword extraction (most intelligent)
        keyword_matches = self.extract_keywords(user_input, valid_options)
        if keyword_matches:
            best_keyword, confidence = keyword_matches[0]
            if confidence >= 0.7:  # 70% confidence
                return best_keyword, int(confidence * 100)
        
        # Fallback to fuzzy matching
        try:
            # Get matches with different scorers
            match1 = process.extractOne(
                user_input, valid_options, scorer=fuzz.ratio
            )
            
            match2 = process.extractOne(
                user_input, valid_options, scorer=fuzz.partial_ratio
            )
            
            match3 = process.extractOne(
                user_input, valid_options, scorer=fuzz.token_sort_ratio
            )
            
            # Each match is a tuple: (text, score, index) - we only need text and score
            matches = []
            if match1:
                matches.append((match1[0], match1[1]))
            if match2:
                matches.append((match2[0], match2[1]))
            if match3:
                matches.append((match3[0], match3[1]))
            
            if not matches:
                return None, 0
            
            # Take the best match
            best_match = max(matches, key=lambda x: x[1])
            
            if best_match[1] >= threshold:
                return best_match[0], best_match[1]
            
            return None, best_match[1]
            
        except Exception as e:
            print(f"Fuzzy matching error: {e}")
            return None, 0
    
    def extract_dietary_restrictions(self, text: str) -> List[str]:
        """Extract dietary restrictions from text"""
        restrictions = []
        
        restriction_keywords = {
            'vegan': ['vegan'],
            'gluten-free': ['gluten free', 'gluten-free', 'celiac'],
            'dairy-free': ['dairy free', 'dairy-free', 'lactose'],
            'nut-free': ['nut free', 'nut-free', 'no nuts', 'allergy'],
            'low-carb': ['low carb', 'keto', 'atkins'],
            'spicy': ['spicy', 'hot', 'chili'],
            'non-spicy': ['not spicy', 'mild', 'no spice']
        }
        
        text_lower = text.lower()
        
        for restriction, keywords in restriction_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                restrictions.append(restriction)
        
        return restrictions
    
    def is_expressing_confusion(self, text: str) -> bool:
        """Detect if user is expressing confusion or doesn't understand"""
        confusion_phrases = [
            "don't understand",
            "what do you mean",
            "confused",
            "not clear",
            "explain",
            "what",
            "huh",
            "repeat",
            "say that again",
            "pardon"
        ]
        
        text_lower = text.lower()
        return any(phrase in text_lower for phrase in confusion_phrases)
    
    def is_negative_response(self, text: str) -> bool:
        """Check if response is negative (no, nope, etc.)"""
        negative_words = ['no', 'nope', 'nah', 'not really', 'don\'t', 'none']
        text_lower = text.lower()
        
        # Check for negative words at the start or as standalone
        words = text_lower.split()
        if words and words[0] in negative_words:
            return True
        
        return any(word == text_lower for word in negative_words)


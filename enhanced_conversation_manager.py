# from typing import Optional, List, Dict, Tuple
# import random

# class EnhancedConversationManager:
#     def __init__(self, data_processor, speech_handler, nlp_engine, context_manager):
#         self.dp = data_processor
#         self.sh = speech_handler
#         self.nlp = nlp_engine
#         self.context = context_manager
        
#         # Configuration
#         self.max_retries = 3
#         self.confidence_threshold = 0.75
#         self.high_confidence_threshold = 0.85
        
#         # Response templates for natural conversation
#         self.greetings = [
#             "Hi! I am Dauna, your personal recipe assistant.",
#             "Hello! I'm Dauna, here to help you find delicious recipes.",
#             "Hi there! Dauna here, ready to discover great recipes with you."
#         ]
        
#         self.confirmations = [
#             "Great choice!",
#             "Excellent!",
#             "Perfect!",
#             "Wonderful!"
#         ]
        
#         self.thinking_phrases = [
#             "Let me find that for you...",
#             "Searching through my recipe collection...",
#             "Give me just a moment...",
#             "Looking that up for you..."
#         ]
    
#     def speak_with_personality(self, message: str, message_type: str = "normal"):
#         """Speak with varied tone based on context"""
#         if message_type == "greeting":
#             self.sh.speak(message, rate=145)
#         elif message_type == "excited":
#             self.sh.speak(message, rate=155)
#         elif message_type == "apologetic":
#             self.sh.speak(message, rate=140)
#         else:
#             self.sh.speak(message)
    
#     def get_user_input_with_confirmation(self, 
#                                         prompt: str, 
#                                         valid_options: List[str],
#                                         retry_message: str,
#                                         context_info: str = "") -> Tuple[Optional[str], float]:
#         """Get user input with intelligent retry and confirmation"""
#         retries = 0
        
#         while retries < self.max_retries:
#             if retries == 0:
#                 self.speak_with_personality(prompt)
#             else:
#                 self.speak_with_personality(retry_message, "apologetic")
            
#             # Listen to user
#             user_input, confidence = self.sh.listen(timeout=8)
            
#             if not user_input:
#                 retries += 1
#                 self.context.current_session['retry_count'] += 1
#                 continue
            
#             # Log conversation
#             self.context.add_to_history("user", user_input, {"confidence": confidence})
            
#             # Analyze sentiment
#             sentiment = self.nlp.analyze_sentiment(user_input)
#             self.context.current_session['user_sentiment'] = sentiment['label'].lower()
            
#             # If user seems frustrated, be more helpful
#             if sentiment['label'] == 'NEGATIVE' and retries > 0:
#                 self.sh.speak("I sense you might be frustrated. Let me try to help better.")
            
#             # Fuzzy match with valid options
#             matched_option, score = self.nlp.fuzzy_match(
#                 user_input, 
#                 valid_options,
#                 threshold=65  # Lower threshold for better UX
#             )
            
#             if matched_option:
#                 # If confidence is low, confirm understanding
#                 if confidence < self.high_confidence_threshold or score < 80:
#                     if self.sh.confirm_understanding(matched_option):
#                         self.context.add_to_history("assistant", f"Confirmed: {matched_option}")
#                         return matched_option, confidence
#                     else:
#                         retries += 1
#                         continue
#                 else:
#                     # High confidence, proceed
#                     return matched_option, confidence
#             else:
#                 # No good match found
#                 if score > 50:  # Close match
#                     self.sh.speak(f"Did you mean {valid_options[0]}? Please clarify.")
                
#                 retries += 1
#                 self.context.current_session['retry_count'] += 1
        
#         return None, 0.0
    
#     def present_recipes_intelligently(self, recipes: List[Dict]) -> List[str]:
#         """Present recipes in a smart way based on user profile"""
#         if not recipes:
#             return []
        
#         recipe_names = [r['name'] for r in recipes]
        
#         # If user has favorites, prioritize similar recipes
#         if self.context.should_suggest_personalized():
#             self.sh.speak("Based on your previous selections, I've ranked these for you.")
#             # Here you could implement ranking logic
        
#         # Limit to top 5 for better UX
#         if len(recipe_names) > 5:
#             self.sh.speak(f"I found {len(recipe_names)} recipes. Let me share the top 5 with you.")
#             recipe_names = recipe_names[:5]
        
#         # Present recipes with brief descriptions
#         recipes_text = ", ".join(recipe_names)
        
#         return recipe_names
    
#     def handle_dietary_restrictions(self) -> List[str]:
#         """Ask about dietary restrictions"""
#         self.sh.speak("Do you have any dietary restrictions? For example, vegan, gluten-free, nut-free, or none?")
        
#         response, conf = self.sh.listen(timeout=8)
        
#         restrictions = []
#         if response:
#             if 'none' in response or 'no' in response:
#                 return restrictions
            
#             restrictions = self.nlp.extract_dietary_restrictions(response)
            
#             if restrictions:
#                 self.sh.speak(f"Noted. I'll avoid recipes with {', '.join(restrictions)}.")
        
#         return restrictions
    
#     def run_enhanced_conversation(self):
#         """Main conversation flow with enhancements"""
        
#         # === GREETING ===
#         greeting = random.choice(self.greetings)
#         self.speak_with_personality(greeting, "greeting")
#         self.context.add_to_history("assistant", greeting)
#         self.context.current_session['current_stage'] = 'diet_selection'
        
#         # Check if returning user
#         if self.context.user_profile['favorite_recipes']:
#             self.sh.speak(f"Welcome back! I remember you liked {self.context.user_profile['favorite_recipes'][0]} last time.")
        
#         # === STEP 1: DIET PREFERENCE ===
#         self.sh.speak("What would you like to search for - Vegetarian or Non-vegetarian?")
        
#         diet_options = ['vegetarian', 'non-vegetarian', 'non vegetarian']
#         diet, diet_conf = self.get_user_input_with_confirmation(
#             "",
#             diet_options,
#             "Sorry, I couldn't understand. Could you please say vegetarian or non-vegetarian?"
#         )
        
#         if not diet:
#             self.sh.speak("I'm having trouble understanding. Let's try again later. Goodbye!")
#             return
        
#         # Normalize
#         diet = 'vegetarian' if 'vegetarian' in diet and 'non' not in diet else 'non-vegetarian'
#         self.context.current_session['diet_preference'] = diet
#         self.context.add_to_history("assistant", f"Diet selected: {diet}")
        
#         # === STEP 2: DIETARY RESTRICTIONS (Optional) ===
#         restrictions = self.handle_dietary_restrictions()
        
#         # === STEP 3: COURSE TYPE ===
#         self.context.current_session['current_stage'] = 'course_selection'
        
#         confirmation = random.choice(self.confirmations)
#         course_prompt = f"{confirmation} For {diet} dishes, what course would you like - main course, snack, or dessert?"
        
#         course_options = ['main course', 'snack', 'dessert', 'main', 'starter']
#         course, course_conf = self.get_user_input_with_confirmation(
#             course_prompt,
#             course_options,
#             "I didn't catch that. Please say main course, snack, or dessert."
#         )
        
#         if not course:
#             self.sh.speak("Let's try again another time. Goodbye!")
#             return
        
#         # Normalize
#         if 'main' in course:
#             course = 'main course'
        
#         self.context.current_session['course_preference'] = course
        
#         # === CONFIRMATION ===
#         summary = f"Perfect! So you're looking for {diet} {course} recipes."
#         self.speak_with_personality(summary, "excited")
#         self.context.add_to_history("assistant", summary)
        
#         # === STEP 4: STATE/REGION ===
#         self.context.current_session['current_stage'] = 'state_selection'
        
#         states = self.dp.df['state'].unique().tolist()
#         states = [s for s in states if s not in ['Unknown', 'Pan-India']]
        
#         # Check user's preferred states
#         if self.context.user_profile['preferred_states']:
#             preferred = self.context.user_profile['preferred_states'][0]
#             self.sh.speak(f"I remember you like recipes from {preferred}. Would you like to search there again, or try a different state?")
            
#             response, _ = self.sh.listen(timeout=6)
#             if response and any(word in response for word in ['yes', 'yeah', 'sure', 'again']):
#                 state = preferred
#             else:
#                 state_list = ", ".join(states[:6])  # Limit for brevity
#                 state_prompt = f"Which state would you like? Options include {state_list}, or you can say any Indian state."
                
#                 state, state_conf = self.get_user_input_with_confirmation(
#                     state_prompt,
#                     states,
#                     "Sorry, I didn't catch the state name. Could you repeat it?"
#                 )
#         else:
#             state_list = ", ".join(states[:6])
#             state_prompt = f"From which state would you like to explore? Some options are {state_list}."
            
#             state, state_conf = self.get_user_input_with_confirmation(
#                 state_prompt,
#                 states,
#                 "I didn't understand the state. Please try again."
#             )
        
#         if not state:
#             self.sh.speak("No worries, let's search across all regions!")
#             state = None
#         else:
#             self.context.current_session['state_preference'] = state
#             # Add to preferred states
#             if state not in self.context.user_profile['preferred_states']:
#                 self.context.user_profile['preferred_states'].append(state)
#                 self.context.save_user_profile()
        
#         # === STEP 5: FILTER AND PRESENT RECIPES ===
#         self.context.current_session['current_stage'] = 'recipe_selection'
        
#         thinking = random.choice(self.thinking_phrases)
#         self.sh.speak(thinking)
        
#         # Advanced filtering
#         filtered_recipes = self.dp.advanced_filter(
#             diet=diet,
#             course=course,
#             state=state,
#             ingredients_exclude=[r.replace('-free', '') for r in restrictions if 'free' in r]
#         )
        
#         if filtered_recipes.empty:
#             self.sh.speak("I couldn't find recipes matching all your criteria. Let me broaden the search.")
            
#             # Retry without state filter
#             filtered_recipes = self.dp.advanced_filter(
#                 diet=diet,
#                 course=course
#             )
        
#         if filtered_recipes.empty:
#             self.sh.speak("I'm sorry, I couldn't find any matching recipes. Would you like to try different criteria?")
#             return
        
#         # Convert to list of dicts
#         recipes_list = filtered_recipes.to_dict('records')
#         self.context.current_session['filtered_recipes'] = recipes_list
        
#         # Present recipes
#         recipe_names = self.present_recipes_intelligently(recipes_list)
        
#         recipes_text = ", ".join(recipe_names)
#         self.sh.speak(f"Here are your options: {recipes_text}. Which one interests you?")
        
#         # === STEP 6: RECIPE SELECTION ===
#         selected_recipe, recipe_conf = self.get_user_input_with_confirmation(
#             "",
#             recipe_names,
#             "Sorry, I didn't catch which recipe you want. Could you repeat the name?"
#         )
        
#         if not selected_recipe:
#             self.sh.speak("No problem. Feel free to ask me anytime. Goodbye!")
#             return
        
#         self.context.current_session['selected_recipe'] = selected_recipe
        
#         # === STEP 7: PROVIDE RECIPE DETAILS ===
#         self.context.current_session['current_stage'] = 'recipe_details'
        
#         recipe_data = filtered_recipes[filtered_recipes['name'] == selected_recipe].iloc[0]
        
#         # Log interaction
#         self.context.log_interaction(int(recipe_data['recipe_id']), 'viewed')
        
#         # Present details
#         ingredients = recipe_data['ingredients']
#         cook_time = recipe_data['cook_time']
#         prep_time = recipe_data['prep_time']
#         total_time = recipe_data['total_time']
#         difficulty = recipe_data['difficulty']
        
#         details = f"Great choice! {selected_recipe} is a {recipe_data['flavor_profile']} dish. "
#         details += f"The total time is {total_time} minutes - {prep_time} minutes prep and {cook_time} minutes cooking. "
#         details += f"Difficulty level is {difficulty} out of 10. "
#         details += f"The main ingredients are: {ingredients}."
        
#         self.speak_with_personality(details)
#         self.context.add_to_history("assistant", details)
        
#         # === STEP 8: ADDITIONAL OPTIONS ===
#         self.sh.speak("Would you like to know anything else? I can suggest similar recipes, provide cooking tips, or start a new search.")
        
#         response, _ = self.sh.listen(timeout=8)
        
#         if response:
#             intent, intent_conf = self.nlp.analyze_intent(response)
            
#             if intent == 'find_similar' or 'similar' in response:
#                 # Find similar recipes
#                 similar = self.dp.get_similar_recipes(selected_recipe, top_k=3)
#                 if similar:
#                     similar_names = [r['name'] for r in similar]
#                     self.sh.speak(f"Similar recipes you might like: {', '.join(similar_names)}.")
            
#             elif intent == 'search_recipe' or any(word in response for word in ['another', 'more', 'different']):
#                 self.sh.speak("Sure! Let's find another recipe.")
#                 self.context.reset_session()
#                 self.run_enhanced_conversation()
#                 return
            
#             elif any(word in response for word in ['like', 'love', 'favorite']):
#                 self.context.update_preferences(selected_recipe, liked=True)
#                 self.sh.speak("I'm glad you liked it! I'll remember that for next time.")
        
#         # === FAREWELL ===
#         farewell_messages = [
#             "It was a pleasure helping you! Hope the recipe turns out delicious. Goodbye!",
#             "Enjoy cooking! Feel free to come back anytime. Goodbye!",
#             "Happy cooking! I hope you love the dish. See you next time!"
#         ]
        
#         self.speak_with_personality(random.choice(farewell_messages), "greeting")
        
#         # Save session data
#         self.context.save_user_profile()



































from typing import Optional, List, Dict, Tuple
import random
from logger_config import logger

class EnhancedConversationManager:
    def __init__(self, data_processor, speech_handler, nlp_engine, context_manager):
        self.dp = data_processor
        self.sh = speech_handler
        self.nlp = nlp_engine
        self.context = context_manager
        
        # Configuration
        self.max_retries = 4  # Increased retries
        self.confidence_threshold = 0.65  # Lowered threshold
        self.high_confidence_threshold = 0.85
        
        # Response templates for natural conversation
        self.greetings = [
            "Hi! I am Donna, your personal recipe assistant.",
            "Hello! I'm Donna, here to help you find delicious recipes.",
            "Hi there! Donna here, ready to discover great recipes with you."
        ]
        
        self.confirmations = [
            "Great choice!",
            "Excellent!",
            "Perfect!",
            "Wonderful!"
        ]
        
        self.thinking_phrases = [
            "Let me find that for you...",
            "Searching through my recipe collection...",
            "Give me just a moment...",
            "Looking that up for you..."
        ]
        
        self.confusion_responses = [
            "I'm not quite sure I understood that. Let me ask again.",
            "Hmm, I didn't catch that clearly. Could you try once more?",
            "I want to make sure I get this right. Let's try again.",
            "Sorry, I'm having trouble understanding. One more time, please?"
        ]
    
    def speak_with_personality(self, message: str, message_type: str = "normal"):
        """Speak with varied tone based on context"""
        if message_type == "greeting":
            self.sh.speak(message, rate=145)
        elif message_type == "excited":
            self.sh.speak(message, rate=155)
        elif message_type == "apologetic":
            self.sh.speak(message, rate=140)
        else:
            self.sh.speak(message)
    
    # def get_user_input_with_intelligence(self, 
    #                                     prompt: str, 
    #                                     valid_options: List[str],
    #                                     context_hint: str = "",
    #                                     allow_partial: bool = True) -> Tuple[Optional[str], float]:
    #     """
    #     Intelligent input handler that:
    #     - Extracts keywords from sentences
    #     - Handles confusion gracefully
    #     - Never terminates abruptly
    #     - Provides helpful feedback
    #     """
    #     retries = 0
    #     last_score = 0
        
    #     while retries < self.max_retries:
    #         # Speak prompt on first try or after confusion
    #         if retries == 0:
    #             self.speak_with_personality(prompt)
    #         else:
    #             # Provide helpful retry message
    #             confusion_msg = random.choice(self.confusion_responses)
    #             self.speak_with_personality(confusion_msg, "apologetic")
                
    #             # Give examples on 2nd+ retry
    #             if retries >= 1:
    #                 examples = valid_options[:3] if len(valid_options) > 3 else valid_options
    #                 self.sh.speak(f"For example, you could say: {', or '.join(examples)}.")
            
    #         # Listen to user
    #         user_input, asr_confidence = self.sh.listen(timeout=10)
            
    #         # Handle no input
    #         if not user_input:
    #             retries += 1
    #             self.context.current_session['retry_count'] += 1
                
    #             if retries < self.max_retries:
    #                 self.sh.speak("I didn't hear anything. Please try speaking again.")
    #             continue
            
    #         print(f"🧠 AI Analysis: Input='{user_input}', ASR Confidence={asr_confidence:.2f}")
            
    #         # Log conversation
    #         self.context.add_to_history("user", user_input, {"confidence": asr_confidence})
            
    #         # Check if user is expressing confusion
    #         if self.nlp.is_expressing_confusion(user_input):
    #             self.sh.speak(f"No problem! I'm asking about {context_hint}. Let me explain the options.")
    #             options_text = ", ".join(valid_options)
    #             self.sh.speak(f"Your options are: {options_text}. Which one would you prefer?")
    #             retries += 1
    #             continue
            
    #         # Analyze sentiment to detect frustration
    #         sentiment = self.nlp.analyze_sentiment(user_input)
    #         self.context.current_session['user_sentiment'] = sentiment['label'].lower()
            
    #         if sentiment['label'] == 'NEGATIVE' and retries > 1:
    #             self.sh.speak("I understand this might be frustrating. Let me help you better.")
            
    #         # INTELLIGENT KEYWORD EXTRACTION
    #         print(f"🔍 Extracting keywords from: '{user_input}'")
    #         print(f"📋 Valid options: {valid_options}")
            
    #         matched_option, match_score = self.nlp.fuzzy_match(
    #             user_input, 
    #             valid_options,
    #             threshold=60  # Lower threshold for better UX
    #         )
            
    #         print(f"✨ Match result: '{matched_option}' with score {match_score}")
            
    #         if matched_option:
    #             # We found a match!
    #             confidence_level = "high" if match_score >= 80 else "medium" if match_score >= 70 else "low"
    #             print(f"✅ Match confidence: {confidence_level} ({match_score})")
                
    #             # For high confidence, proceed directly
    #             if match_score >= 85 and asr_confidence >= 0.75:
    #                 self.context.add_to_history("assistant", f"Understood: {matched_option}")
    #                 return matched_option, asr_confidence
                
    #             # For medium confidence, confirm with user
    #             elif match_score >= 70:
    #                 self.sh.speak(f"I heard {matched_option}. Is that correct?")
    #                 confirmation, _ = self.sh.listen(timeout=6)
                    
    #                 if confirmation:
    #                     # Check for positive confirmation
    #                     if any(word in confirmation.lower() for word in ['yes', 'yeah', 'correct', 'right', 'yep', 'sure']):
    #                         self.context.add_to_history("assistant", f"Confirmed: {matched_option}")
    #                         return matched_option, asr_confidence
    #                     elif any(word in confirmation.lower() for word in ['no', 'nope', 'wrong', 'not']):
    #                         self.sh.speak("My apologies. Let me ask again.")
    #                         retries += 1
    #                         continue
                    
    #                 # If no clear confirmation, ask again
    #                 self.sh.speak("Let me ask once more to be sure.")
    #                 retries += 1
    #                 continue
                
    #             # For low confidence, give feedback
    #             else:
    #                 self.sh.speak(f"I think you might have said {matched_option}, but I'm not certain.")
    #                 self.sh.speak(f"Could you please say it more clearly? Your options are: {', '.join(valid_options)}.")
    #                 retries += 1
    #                 last_score = match_score
    #                 continue
            
    #         else:
    #             # No match found
    #             print(f"❌ No match found (best score was {match_score})")
                
    #             # Provide helpful feedback
    #             if last_score > 0 and match_score > last_score:
    #                 self.sh.speak("Getting closer, but I'm still not quite getting it.")
                
    #             # Show what we're looking for
    #             if retries >= 2:
    #                 self.sh.speak(f"I'm specifically looking for one of these: {', '.join(valid_options)}.")
    #                 self.sh.speak("Please choose one from these options.")
                
    #             retries += 1
    #             last_score = match_score
        
    #     # Max retries reached - but DON'T terminate!
    #     self.sh.speak("I'm having persistent trouble understanding this particular question.")
    #     self.sh.speak("Would you like to skip this and try something else, or shall we try again?")
        
    #     skip_response, _ = self.sh.listen(timeout=6)
        
    #     if skip_response and any(word in skip_response.lower() for word in ['skip', 'else', 'different', 'another']):
    #         return None, 0.0
    #     else:
    #         self.sh.speak("Alright, let's give it one more focused try.")
    #         # Recursive call with fresh retries
    #         return self.get_user_input_with_intelligence(prompt, valid_options, context_hint, allow_partial)
    
    def get_user_input_with_intelligence(self, 
                                        prompt: str, 
                                        valid_options: List[str],
                                        context_hint: str = "",
                                        allow_partial: bool = True) -> Tuple[Optional[str], float]:
        """
        Intelligent input handler with comprehensive logging
        """
        logger.info(f"Requesting input - Context: {context_hint}")
        logger.info(f"Valid options: {valid_options}")
        
        retries = 0
        last_score = 0
        
        while retries < self.max_retries:
            # Speak prompt on first try or after confusion
            if retries == 0:
                self.speak_with_personality(prompt)
            else:
                # Provide helpful retry message
                confusion_msg = random.choice(self.confusion_responses)
                self.speak_with_personality(confusion_msg, "apologetic")
                logger.warning(f"Retry attempt {retries}/{self.max_retries}")
                
                # Give examples on 2nd+ retry
                if retries >= 1:
                    examples = valid_options[:3] if len(valid_options) > 3 else valid_options
                    example_text = f"For example, you could say: {', or '.join(examples)}."
                    self.sh.speak(example_text)
                    logger.info(f"Providing examples: {examples}")
            
            # Listen to user
            user_input, asr_confidence = self.sh.listen(timeout=10)
            
            # Handle no input
            if not user_input:
                retries += 1
                self.context.current_session['retry_count'] += 1
                logger.warning(f"No input detected (attempt {retries})")
                
                if retries < self.max_retries:
                    self.sh.speak("I didn't hear anything. Please try speaking again.")
                continue
            
            logger.info(f"User input: '{user_input}' (ASR confidence: {asr_confidence:.2f})")
            print(f"🧠 AI Analysis: Input='{user_input}', ASR Confidence={asr_confidence:.2f}")
            
            # Log conversation
            self.context.add_to_history("user", user_input, {"confidence": asr_confidence})
            
            # Check if user is expressing confusion
            if self.nlp.is_expressing_confusion(user_input):
                logger.info("User expressing confusion - providing clarification")
                self.sh.speak(f"No problem! I'm asking about {context_hint}. Let me explain the options.")
                options_text = ", ".join(valid_options)
                self.sh.speak(f"Your options are: {options_text}. Which one would you prefer?")
                retries += 1
                continue
            
            # Analyze sentiment to detect frustration
            sentiment = self.nlp.analyze_sentiment(user_input)
            self.context.current_session['user_sentiment'] = sentiment['label'].lower()
            logger.info(f"Sentiment: {sentiment['label']} (score: {sentiment['score']:.2f})")
            
            if sentiment['label'] == 'NEGATIVE' and retries > 1:
                self.sh.speak("I understand this might be frustrating. Let me help you better.")
                logger.warning("User showing signs of frustration")
            
            # INTELLIGENT KEYWORD EXTRACTION
            logger.info(f"Extracting keywords from: '{user_input}'")
            print(f"🔍 Extracting keywords from: '{user_input}'")
            print(f"📋 Valid options: {valid_options}")
            
            matched_option, match_score = self.nlp.fuzzy_match(
                user_input, 
                valid_options,
                threshold=60  # Lower threshold for better UX
            )
            
            logger.info(f"Match result: '{matched_option}' (score: {match_score})")
            print(f"✨ Match result: '{matched_option}' with score {match_score}")
            
            if matched_option:
                # We found a match!
                confidence_level = "high" if match_score >= 80 else "medium" if match_score >= 70 else "low"
                logger.info(f"Match confidence: {confidence_level} ({match_score})")
                print(f"✅ Match confidence: {confidence_level} ({match_score})")
                
                # For high confidence, proceed directly
                if match_score >= 85 and asr_confidence >= 0.75:
                    logger.info(f"High confidence match accepted: {matched_option}")
                    self.context.add_to_history("assistant", f"Understood: {matched_option}")
                    return matched_option, asr_confidence
                
                # For medium confidence, confirm with user
                elif match_score >= 70:
                    logger.info(f"Medium confidence - requesting confirmation")
                    self.sh.speak(f"I heard {matched_option}. Is that correct?")
                    confirmation, _ = self.sh.listen(timeout=6)
                    
                    if confirmation:
                        logger.info(f"Confirmation response: '{confirmation}'")
                        # Check for positive confirmation
                        if any(word in confirmation.lower() for word in ['yes', 'yeah', 'correct', 'right', 'yep', 'sure', 'yup']):
                            logger.info(f"User confirmed: {matched_option}")
                            self.context.add_to_history("assistant", f"Confirmed: {matched_option}")
                            return matched_option, asr_confidence
                        elif any(word in confirmation.lower() for word in ['no', 'nope', 'wrong', 'not', 'nah']):
                            logger.info("User rejected match - retrying")
                            self.sh.speak("My apologies. Let me ask again.")
                            retries += 1
                            continue
                    
                    # If no clear confirmation, ask again
                    logger.warning("Unclear confirmation - retrying")
                    self.sh.speak("Let me ask once more to be sure.")
                    retries += 1
                    continue
                
                # For low confidence, give feedback
                else:
                    logger.warning(f"Low confidence match ({match_score}) - seeking clarification")
                    self.sh.speak(f"I think you might have said {matched_option}, but I'm not certain.")
                    self.sh.speak(f"Could you please say it more clearly? Your options are: {', '.join(valid_options)}.")
                    retries += 1
                    last_score = match_score
                    continue
            
            else:
                # No match found
                logger.warning(f"No match found (best score: {match_score})")
                print(f"❌ No match found (best score was {match_score})")
                
                # Provide helpful feedback
                if last_score > 0 and match_score > last_score:
                    self.sh.speak("Getting closer, but I'm still not quite getting it.")
                    logger.info("Progress detected in user input")
                
                # Show what we're looking for
                if retries >= 2:
                    self.sh.speak(f"I'm specifically looking for one of these: {', '.join(valid_options)}.")
                    self.sh.speak("Please choose one from these options.")
                
                retries += 1
                last_score = match_score
        
        # Max retries reached - but DON'T terminate!
        logger.error(f"Max retries reached for context: {context_hint}")
        self.sh.speak("I'm having persistent trouble understanding this particular question.")
        self.sh.speak("Would you like to skip this and try something else, or shall we try again?")
        
        skip_response, _ = self.sh.listen(timeout=6)
        logger.info(f"Skip/retry response: '{skip_response}'")
        
        if skip_response and any(word in skip_response.lower() for word in ['skip', 'else', 'different', 'another']):
            logger.info("User chose to skip this question")
            return None, 0.0
        else:
            logger.info("User chose to retry - making recursive call")
            self.sh.speak("Alright, let's give it one more focused try.")
            # Recursive call with fresh retries
            return self.get_user_input_with_intelligence(prompt, valid_options, context_hint, allow_partial)


    def run_enhanced_conversation(self):
        """Main conversation flow with enhanced intelligence and no abrupt terminations"""
        
        try:
            # === GREETING ===
            greeting = random.choice(self.greetings)
            self.speak_with_personality(greeting, "greeting")
            self.context.add_to_history("assistant", greeting)
            self.context.current_session['current_stage'] = 'diet_selection'
            
            # Check if returning user
            if self.context.user_profile['favorite_recipes']:
                self.sh.speak(f"Welcome back! I remember you liked {self.context.user_profile['favorite_recipes'][0]} last time.")
            
            # === STEP 1: DIET PREFERENCE ===
            self.sh.speak("What would you like to search for - Vegetarian or Non-vegetarian?")
            
            diet_options = ['vegetarian', 'non-vegetarian']
            diet, diet_conf = self.get_user_input_with_intelligence(
                "",
                diet_options,
                context_hint="dietary preference - vegetarian or non-vegetarian"
            )
            
            if not diet:
                self.sh.speak("No problem! Would you like to see all recipes regardless of diet type?")
                response, _ = self.sh.listen(timeout=6)
                
                if response and any(word in response.lower() for word in ['yes', 'yeah', 'sure', 'okay']):
                    diet = None  # Show all
                else:
                    self.sh.speak("Let's try the diet selection one more time.")
                    # Retry instead of exit
                    self.run_enhanced_conversation()
                    return
            
            # Normalize diet
            if diet:
                diet = 'vegetarian' if 'vegetarian' in diet and 'non' not in diet else 'non vegetarian'
                self.context.current_session['diet_preference'] = diet
                self.context.add_to_history("assistant", f"Diet selected: {diet}")
            
            # === STEP 2: DIETARY RESTRICTIONS (Optional) ===
            restrictions = self.handle_dietary_restrictions()
            
            # === STEP 3: COURSE TYPE ===
            self.context.current_session['current_stage'] = 'course_selection'
            
            confirmation = random.choice(self.confirmations)
            if diet:
                course_prompt = f"{confirmation} For {diet} dishes, what course would you like - main course, snack, or dessert?"
            else:
                course_prompt = f"{confirmation} What course would you like - main course, snack, or dessert?"
            
            course_options = ['main course', 'snack', 'dessert']
            course, course_conf = self.get_user_input_with_intelligence(
                course_prompt,
                course_options,
                context_hint="type of course - main course, snack, or dessert"
            )
            
            if not course:
                self.sh.speak("Would you like to see recipes from all courses?")
                response, _ = self.sh.listen(timeout=6)
                
                if response and any(word in response.lower() for word in ['yes', 'yeah', 'sure']):
                    course = None
                else:
                    # Retry course selection
                    self.sh.speak("Let's try selecting the course again.")
                    course, course_conf = self.get_user_input_with_intelligence(
                        "Please tell me - would you like main course, snack, or dessert?",
                        course_options,
                        context_hint="course type"
                    )
            
            if course:
                self.context.current_session['course_preference'] = course
            
            # === CONFIRMATION ===
            summary_parts = []
            if diet:
                summary_parts.append(f"{diet}")
            if course:
                summary_parts.append(f"{course}")
            
            if summary_parts:
                summary = f"Perfect! So you're looking for {' '.join(summary_parts)} recipes."
            else:
                summary = "Great! Let's find some delicious recipes for you."
            
            self.speak_with_personality(summary, "excited")
            self.context.add_to_history("assistant", summary)
            
            # Continue with rest of conversation...
            # [Rest of the conversation flow continues as before]
            # === STEP 4: STATE/REGION ===
            self.context.current_session['current_stage'] = 'state_selection'
            
            states = self.dp.df['state'].unique().tolist()
            states = [s for s in states if s not in ['Unknown', 'Pan-India']]
            
            state_list = ", ".join(states[:6])
            state_prompt = f"From which state would you like to explore? Some options are {state_list}."
            
            state, state_conf = self.get_user_input_with_intelligence(
                state_prompt,
                states,
                context_hint="Indian state for regional cuisine"
            )
            
            if state:
                self.context.current_session['state_preference'] = state
                if state not in self.context.user_profile['preferred_states']:
                    self.context.user_profile['preferred_states'].append(state)
                    self.context.save_user_profile()
            else:
                self.sh.speak("No problem! I'll search across all regions.")
            
            # === STEP 5: FILTER AND PRESENT RECIPES ===
            self.filter_and_present_recipes(diet, course, state, restrictions)
            
        except Exception as e:
            print(f"Error in conversation: {e}")
            import traceback
            traceback.print_exc()
            
            # Don't terminate - offer to restart
            self.sh.speak("Oops! I encountered a small hiccup. Would you like to start over?")
            response, _ = self.sh.listen(timeout=6)
            
            if response and any(word in response.lower() for word in ['yes', 'yeah', 'sure']):
                self.context.reset_session()
                self.run_enhanced_conversation()
    
    def filter_and_present_recipes(self, diet, course, state, restrictions):
        """Filter recipes and present to user"""
        self.context.current_session['current_stage'] = 'recipe_selection'
        
        thinking = random.choice(self.thinking_phrases)
        self.sh.speak(thinking)
        
        # Advanced filtering
        filtered_recipes = self.dp.advanced_filter(
            diet=diet,
            course=course,
            state=state,
            ingredients_exclude=[r.replace('-free', '') for r in restrictions if 'free' in r]
        )
        
        if filtered_recipes.empty:
            self.sh.speak("I couldn't find recipes matching all your criteria. Let me broaden the search.")
            filtered_recipes = self.dp.advanced_filter(diet=diet, course=course)
        
        if filtered_recipes.empty:
            self.sh.speak("I'm sorry, I couldn't find any matching recipes. Would you like to try different criteria?")
            
            response, _ = self.sh.listen(timeout=6)
            if response and any(word in response.lower() for word in ['yes', 'yeah', 'sure']):
                self.context.reset_session()
                self.run_enhanced_conversation()
            return
        
        # Present recipes
        recipes_list = filtered_recipes.to_dict('records')
        recipe_names = [r['name'] for r in recipes_list[:5]]
        
        recipes_text = ", ".join(recipe_names)
        self.sh.speak(f"Here are your options: {recipes_text}. Which one interests you?")
        
        # Get recipe selection
        selected_recipe, _ = self.get_user_input_with_intelligence(
            "",
            recipe_names,
            context_hint="recipe name from the list I just mentioned"
        )
        
        if not selected_recipe:
            self.sh.speak("Would you like me to repeat the recipe names?")
            response, _ = self.sh.listen(timeout=6)
            
            if response and any(word in response.lower() for word in ['yes', 'yeah', 'sure']):
                self.sh.speak(f"The recipes are: {recipes_text}")
                selected_recipe, _ = self.get_user_input_with_intelligence(
                    "Which one would you like?",
                    recipe_names,
                    context_hint="recipe name"
                )
        
        if selected_recipe:
            self.provide_recipe_details(selected_recipe, filtered_recipes)
        else:
            self.sh.speak("No worries! Feel free to come back anytime. Goodbye!")
    
    # def provide_recipe_details(self, recipe_name, filtered_recipes):
    #     """Provide detailed information about selected recipe"""
    #     recipe_data = filtered_recipes[filtered_recipes['name'] == recipe_name].iloc[0]
        
    #     self.context.log_interaction(int(recipe_data['recipe_id']), 'viewed')
        
    #     ingredients = recipe_data['ingredients']
    #     cook_time = recipe_data['cook_time']
    #     prep_time = recipe_data['prep_time']
    #     total_time = recipe_data['total_time']
        
    #     details = f"Great choice! {recipe_name}. "
    #     details += f"The total time is {total_time} minutes - {prep_time} minutes prep and {cook_time} minutes cooking. "
    #     details += f"The main ingredients are: {ingredients}."
        
    #     self.speak_with_personality(details)
        
    #     # Ask for more
    #     self.sh.speak("Would you like to know anything else?")
    #     response, _ = self.sh.listen(timeout=8)
        
    #     if response and any(word in response.lower() for word in ['yes', 'more', 'another']):
    #         self.context.reset_session()
    #         self.run_enhanced_conversation()
    #     else:
    #         farewell = "It was a pleasure helping you! Enjoy cooking. Goodbye!"
    #         self.speak_with_personality(farewell, "greeting")
    
    def handle_dietary_restrictions(self) -> List[str]:
        """Ask about dietary restrictions"""
        self.sh.speak("Do you have any dietary restrictions? For example, vegan, gluten-free, or none?")
        
        response, conf = self.sh.listen(timeout=8)
        
        restrictions = []
        if response:
            if self.nlp.is_negative_response(response) or 'none' in response.lower():
                return restrictions
            
            restrictions = self.nlp.extract_dietary_restrictions(response)
            
            if restrictions:
                self.sh.speak(f"Noted. I'll avoid recipes with {', '.join(restrictions)}.")
        
        return restrictions

    def provide_recipe_details(self, recipe_name, filtered_recipes):
        """Provide detailed information about selected recipe with enhanced features"""
        try:
            recipe_data = filtered_recipes[filtered_recipes['name'] == recipe_name].iloc[0]
        except IndexError:
            self.sh.speak(f"I'm sorry, I couldn't find the recipe {recipe_name}. Let me search again.")
            return
        
        # Log interaction
        try:
            self.context.log_interaction(int(recipe_data['recipe_id']), 'viewed')
        except:
            pass
        
        # Extract all details
        ingredients = recipe_data['ingredients']
        cook_time = recipe_data['cook_time']
        prep_time = recipe_data['prep_time']
        total_time = recipe_data['total_time']
        difficulty = recipe_data.get('difficulty', 'unknown')
        flavor_profile = recipe_data.get('flavor_profile', 'balanced')
        state = recipe_data.get('state', 'India')
        region = recipe_data.get('region', 'Multi-regional')
        
        # Present basic details
        details = f"Excellent choice! {recipe_name} is a delicious {flavor_profile} dish from {state}. "
        
        # Add difficulty assessment
        if difficulty != 'unknown':
            if difficulty <= 3:
                difficulty_text = "easy"
            elif difficulty <= 6:
                difficulty_text = "moderate"
            else:
                difficulty_text = "challenging"
            details += f"This is a {difficulty_text} recipe. "
        
        # Add timing
        details += f"The total time is about {total_time} minutes - {prep_time} minutes for preparation and {cook_time} minutes for cooking. "
        
        self.speak_with_personality(details)
        
        # Ask what they want to know more about
        self.sh.speak("Would you like to know about the ingredients, cooking tips, or similar recipes?")
        
        response, _ = self.sh.listen(timeout=8)
        
        if response:
            response_lower = response.lower()
            
            # Ingredients request
            if any(word in response_lower for word in ['ingredient', 'ingredients', 'what do i need', 'items']):
                self.sh.speak(f"Here are the ingredients you'll need: {ingredients}")
                
                # Offer substitutions
                self.sh.speak("Would you like suggestions for ingredient substitutions?")
                sub_response, _ = self.sh.listen(timeout=6)
                
                if sub_response and any(word in sub_response.lower() for word in ['yes', 'yeah', 'sure']):
                    self.suggest_ingredient_substitutions(recipe_data)
            
            # Cooking tips request
            elif any(word in response_lower for word in ['tip', 'tips', 'help', 'advice', 'how']):
                self.provide_cooking_tips(recipe_data)
            
            # Similar recipes request
            elif any(word in response_lower for word in ['similar', 'like this', 'recommend', 'other']):
                self.suggest_similar_recipes(recipe_name)
            
            # Nutritional info (if available)
            elif any(word in response_lower for word in ['nutrition', 'calories', 'healthy', 'nutritional']):
                self.sh.speak("I don't have detailed nutritional information, but I can tell you about the main ingredients and their benefits.")
                self.provide_nutritional_insights(recipe_data)
            
            # Full recipe details
            else:
                # Read out ingredients
                self.sh.speak(f"The main ingredients are: {ingredients}")
        
        # Ask about next steps
        self.sh.speak("Is there anything else you'd like to know about this recipe, or shall we search for another one?")
        
        next_response, _ = self.sh.listen(timeout=8)
        
        if next_response:
            if any(word in next_response.lower() for word in ['another', 'different', 'more', 'search', 'new']):
                self.sh.speak("Great! Let's find another delicious recipe.")
                self.context.reset_session()
                self.run_enhanced_conversation()
            elif any(word in next_response.lower() for word in ['similar', 'like this']):
                self.suggest_similar_recipes(recipe_name)
            else:
                # End conversation
                self.end_conversation()
        else:
            self.end_conversation()
    
    def suggest_ingredient_substitutions(self, recipe_data):
        """Suggest common ingredient substitutions"""
        common_substitutions = {
            'ghee': 'You can substitute ghee with butter or oil',
            'paneer': 'Paneer can be substituted with tofu for a vegan option',
            'yogurt': 'Use coconut yogurt or cashew cream as dairy-free alternatives',
            'milk': 'Try almond milk, soy milk, or coconut milk',
            'cashews': 'Almonds or sunflower seeds work as nut-free alternatives',
            'wheat flour': 'Rice flour or almond flour for gluten-free options',
            'sugar': 'Honey, jaggery, or maple syrup are natural alternatives'
        }
        
        ingredients_lower = recipe_data['ingredients'].lower()
        suggestions = []
        
        for ingredient, substitution in common_substitutions.items():
            if ingredient in ingredients_lower:
                suggestions.append(substitution)
        
        if suggestions:
            self.sh.speak("Here are some substitution ideas: " + ". ".join(suggestions[:3]))
        else:
            self.sh.speak("This recipe uses pretty standard ingredients. Most can be substituted based on your dietary needs.")
    
    def provide_cooking_tips(self, recipe_data):
        """Provide cooking tips based on recipe characteristics"""
        tips = []
        
        difficulty = recipe_data.get('difficulty', 5)
        cook_time = recipe_data.get('cook_time', 30)
        flavor = recipe_data.get('flavor_profile', '').lower()
        
        # Time-based tips
        if cook_time > 60:
            tips.append("This dish takes some time, so plan ahead. You can prep ingredients in advance to save time.")
        
        # Difficulty-based tips
        if difficulty > 6:
            tips.append("This is a more challenging recipe. Take your time and follow each step carefully.")
        elif difficulty < 3:
            tips.append("This is a beginner-friendly recipe, perfect for trying something new!")
        
        # Flavor-based tips
        if 'spicy' in flavor:
            tips.append("Adjust the spice level to your preference. Start with less and add more if needed.")
        elif 'sweet' in flavor:
            tips.append("Balance is key with sweet dishes. Don't overdo the sugar.")
        
        # General tips
        tips.append("Always taste as you cook and adjust seasonings to your liking.")
        tips.append("Prepare all ingredients before you start cooking for a smoother experience.")
        
        self.sh.speak("Here are some helpful tips: " + " ".join(tips[:3]))
    
    def suggest_similar_recipes(self, recipe_name):
        """Suggest similar recipes"""
        self.sh.speak("Let me find similar recipes for you...")
        
        try:
            similar = self.dp.get_similar_recipes(recipe_name, top_k=3)
            
            if similar:
                similar_names = [r['name'] for r in similar]
                self.sh.speak(f"You might also enjoy: {', '.join(similar_names)}")
                
                self.sh.speak("Would you like to know more about any of these?")
                response, _ = self.sh.listen(timeout=8)
                
                if response:
                    # Try to match with one of the suggested recipes
                    matched, score = self.nlp.fuzzy_match(response, similar_names, threshold=60)
                    
                    if matched:
                        # Get the full recipe data
                        matched_recipe = next((r for r in similar if r['name'] == matched), None)
                        if matched_recipe:
                            filtered_df = self.dp.df[self.dp.df['name'] == matched]
                            self.provide_recipe_details(matched, filtered_df)
            else:
                self.sh.speak("I couldn't find similar recipes at the moment.")
                
        except Exception as e:
            print(f"Error finding similar recipes: {e}")
            self.sh.speak("I had trouble finding similar recipes. Would you like to search for something else?")
    
    def provide_nutritional_insights(self, recipe_data):
        """Provide basic nutritional insights based on ingredients"""
        ingredients_lower = recipe_data['ingredients'].lower()
        
        insights = []
        
        # Check for healthy ingredients
        if any(word in ingredients_lower for word in ['spinach', 'kale', 'vegetables']):
            insights.append("This dish is rich in vegetables, providing fiber and vitamins.")
        
        if any(word in ingredients_lower for word in ['lentils', 'dal', 'chickpeas', 'beans']):
            insights.append("The legumes provide excellent plant-based protein.")
        
        if 'ghee' in ingredients_lower or 'oil' in ingredients_lower:
            insights.append("Contains healthy fats for energy and nutrient absorption.")
        
        if 'turmeric' in ingredients_lower:
            insights.append("Turmeric has anti-inflammatory properties.")
        
        if 'ginger' in ingredients_lower or 'garlic' in ingredients_lower:
            insights.append("Ginger and garlic boost immunity and aid digestion.")
        
        if insights:
            self.sh.speak(" ".join(insights[:3]))
        else:
            self.sh.speak("This is a traditional recipe with wholesome ingredients that provide balanced nutrition.")
    
    def end_conversation(self):
        """End the conversation gracefully"""
        # Ask for feedback
        self.sh.speak("Before you go, did you find what you were looking for?")
        feedback, _ = self.sh.listen(timeout=6)
        
        if feedback:
            if any(word in feedback.lower() for word in ['yes', 'yeah', 'helpful', 'good', 'great']):
                self.sh.speak("I'm so glad I could help!")
            elif any(word in feedback.lower() for word in ['no', 'not really', "couldn't", 'bad']):
                self.sh.speak("I'm sorry I couldn't help better. I'll keep learning to serve you better next time.")
        
        farewell_messages = [
            "It was a pleasure helping you today! Happy cooking, and enjoy your meal. Goodbye!",
            "Thank you for using Donna! I hope your cooking turns out delicious. See you next time!",
            "Enjoy making this wonderful dish! Feel free to come back anytime. Goodbye!"
        ]
        
        import random
        self.speak_with_personality(random.choice(farewell_messages), "greeting")
        
        # Save user profile
        try:
            self.context.save_user_profile()
        except:
            pass
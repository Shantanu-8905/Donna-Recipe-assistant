from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import sqlite3

class ConversationContext:
    def __init__(self, user_id: str = "default_user", db_path: str = "recipes.db"):
        self.user_id = user_id
        self.db_path = db_path
        self.current_session = {
            'start_time': datetime.now(),
            'diet_preference': None,
            'course_preference': None,
            'state_preference': None,
            'selected_recipe': None,
            'filtered_recipes': [],
            'conversation_history': [],
            'user_sentiment': 'neutral',
            'retry_count': 0,
            'current_stage': 'greeting'
        }
        self.user_profile = self.load_user_profile()
    
    def load_user_profile(self) -> Dict:
        """Load user preferences"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM user_preferences WHERE user_id = ?",
                (self.user_id,)
            )
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'favorite_recipes': json.loads(result[1]) if result[1] else [],
                    'disliked_recipes': json.loads(result[2]) if result[2] else [],
                    'dietary_restrictions': json.loads(result[3]) if result[3] else [],
                    'preferred_states': json.loads(result[4]) if result[4] else [],
                    'avg_cooking_time': result[5],
                    'skill_level': result[6]
                }
            
            return self.create_default_profile()
            
        except Exception as e:
            print(f"Error loading profile: {e}")
            return self.create_default_profile()
    
    def create_default_profile(self) -> Dict:
        """Create a default profile"""
        return {
            'favorite_recipes': [],
            'disliked_recipes': [],
            'dietary_restrictions': [],
            'preferred_states': [],
            'avg_cooking_time': 60,
            'skill_level': 'intermediate'
        }
    
    def save_user_profile(self):
        """Save preferences"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO user_preferences 
                (user_id, favorite_recipes, disliked_recipes, dietary_restrictions,
                 preferred_states, avg_cooking_time, skill_level)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.user_id,
                json.dumps(self.user_profile['favorite_recipes']),
                json.dumps(self.user_profile['disliked_recipes']),
                json.dumps(self.user_profile['dietary_restrictions']),
                json.dumps(self.user_profile['preferred_states']),
                self.user_profile['avg_cooking_time'],
                self.user_profile['skill_level']
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error saving profile: {e}")
    
    def add_to_history(self, role: str, message: str, metadata: Dict = None):
        """Add interaction to conversation history"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'role': role,
            'message': message,
            'metadata': metadata or {}
        }
        self.current_session['conversation_history'].append(entry)
    
    def log_interaction(self, recipe_id: int, action: str):
        """Log user interaction with recipe"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO interactions (user_id, recipe_id, action)
                VALUES (?, ?, ?)
            ''', (self.user_id, recipe_id, action))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error logging interaction: {e}")
    
    def update_preferences(self, recipe_name: str, liked: bool):
        """Update user preferences based on interaction"""
        if liked:
            if recipe_name not in self.user_profile['favorite_recipes']:
                self.user_profile['favorite_recipes'].append(recipe_name)
        else:
            if recipe_name not in self.user_profile['disliked_recipes']:
                self.user_profile['disliked_recipes'].append(recipe_name)
        
        self.save_user_profile()
    
    def get_context_summary(self) -> str:
        """Get summary of current conversation context"""
        summary_parts = []
        
        if self.current_session['diet_preference']:
            summary_parts.append(f"Diet: {self.current_session['diet_preference']}")
        
        if self.current_session['course_preference']:
            summary_parts.append(f"Course: {self.current_session['course_preference']}")
        
        if self.current_session['state_preference']:
            summary_parts.append(f"State: {self.current_session['state_preference']}")
        
        return ", ".join(summary_parts) if summary_parts else "No preferences set"
    
    def should_suggest_personalized(self) -> bool:
        """Determine if personalized suggestions should be made"""
        return len(self.user_profile['favorite_recipes']) > 2
    
    def reset_session(self):
        """Reset current session while keeping user profile"""
        self.current_session = {
            'start_time': datetime.now(),
            'diet_preference': None,
            'course_preference': None,
            'state_preference': None,
            'selected_recipe': None,
            'filtered_recipes': [],
            'conversation_history': [],
            'user_sentiment': 'neutral',
            'retry_count': 0,
            'current_stage': 'greeting'
        }
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import pickle
import sqlite3
from typing import List, Dict, Optional
import re

class AdvancedDataProcessor:
    def __init__(self, dataset_path: str, db_path: str = 'recipes.db'):
        self.dataset_path = dataset_path
        self.db_path = db_path
        self.df = None
        self.embeddings = None
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast model
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000)
        
    def clean_and_enhance_data(self) -> pd.DataFrame:
        """Load or clean the recipe data"""
        import os
        
        # Check for cleaned dataset first
        cleaned_path = self.dataset_path.replace('.csv', '_cleaned.csv')
        
        if os.path.exists(cleaned_path):
            print(f"Loading pre-cleaned dataset from {os.path.basename(cleaned_path)}")
            self.df = pd.read_csv(cleaned_path)
        else:
            print(f"Cleaned dataset not found. Loading and cleaning {os.path.basename(self.dataset_path)}...")
            from data_cleaner import DataCleaner
            
            cleaner = DataCleaner(self.dataset_path)
            self.df = cleaner.clean()
            cleaner.save_cleaned_data()
        
        # Convert ingredient_list from string to actual list if needed
        if self.df['ingredient_list'].dtype == 'object':
            try:
                self.df['ingredient_list'] = self.df['ingredient_list'].apply(
                    lambda x: eval(x) if isinstance(x, str) else x
                )
            except:
                self.df['ingredient_list'] = self.df['ingredients'].apply(
                    lambda x: [i.strip().lower() for i in str(x).split(',')]
                )
        
        # Add unique ID if not present
        if 'recipe_id' not in self.df.columns:
            self.df['recipe_id'] = range(len(self.df))
        
        print(f"✅ Loaded {len(self.df)} recipes with {len(self.df.columns)} features")
        return self.df
    
    def create_embeddings(self):
        """Generate embeddings for semantic search"""
        print("Creating semantic embeddings...")
        
        # Combine name, ingredients, and flavor for embedding
        texts = (
            self.df['name'] + '. Ingredients: ' + 
            self.df['ingredients'] + '. Flavor: ' + 
            self.df['flavor_profile'].fillna('balanced')
        ).tolist()
        
        self.embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Save embeddings
        with open('recipe_embeddings.pkl', 'wb') as f:
            pickle.dump(self.embeddings, f)
    
    def setup_database(self):
        """Set up the database"""
        import sqlite3
        import json
        import numpy as np

        conn = sqlite3.connect(self.db_path)

        # Serialize complex types in the DataFrame
        def serialize_column(val):
            if isinstance(val, np.ndarray):
                return json.dumps(val.tolist())
            elif isinstance(val, (list, dict, set)):
                return json.dumps(list(val) if isinstance(val, set) else val)
            else:
                return val

        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                self.df[col] = self.df[col].apply(serialize_column)

        # Save main recipes table
        self.df.to_sql('recipes', conn, if_exists='replace', index=False)

        # Create indexes for faster queries
        cursor = conn.cursor()
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_diet ON recipes(diet)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_course ON recipes(course)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_state ON recipes(state)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_difficulty ON recipes(difficulty)')

        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id TEXT PRIMARY KEY,
                favorite_recipes TEXT,
                disliked_recipes TEXT,
                dietary_restrictions TEXT,
                preferred_states TEXT,
                avg_cooking_time INTEGER,
                skill_level TEXT,
                last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Interaction history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                recipe_id INTEGER,
                action TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()
        
    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search recipes based on meaning"""
        # Encode query
        query_embedding = self.model.encode([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top matches
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            recipe = self.df.iloc[idx].to_dict()
            recipe['similarity_score'] = float(similarities[idx])
            results.append(recipe)
        
        return results
    
    def advanced_filter(self, 
                       diet: Optional[str] = None,
                       course: Optional[str] = None, 
                       state: Optional[str] = None,
                       max_time: Optional[int] = None,
                       max_difficulty: Optional[float] = None,
                       ingredients_include: Optional[List[str]] = None,
                       ingredients_exclude: Optional[List[str]] = None,
                       flavor_profile: Optional[str] = None) -> pd.DataFrame:
        """Filter recipes by various criteria"""
        
        filtered_df = self.df.copy()
        
        print(f"\n🔍 Filtering recipes:")
        print(f"  Diet: {diet}")
        print(f"  Course: {course}")
        print(f"  State: {state}")
        print(f"  Max time: {max_time}")
        print(f"  Max difficulty: {max_difficulty}")
        print(f"  Include ingredients: {ingredients_include}")
        print(f"  Exclude ingredients: {ingredients_exclude}")
        print(f"  Flavor: {flavor_profile}")
        
        # Filter by diet
        if diet:
            before = len(filtered_df)
            # Normalize diet value to match data format (convert hyphen to space)
            diet_normalized = diet.lower().replace('-', ' ')
            filtered_df = filtered_df[filtered_df['diet'] == diet_normalized]
            print(f"  After diet filter: {len(filtered_df)} recipes (removed {before - len(filtered_df)})")
        
        # Filter by course
        if course:
            before = len(filtered_df)
            filtered_df = filtered_df[filtered_df['course'] == course.lower()]
            print(f"  After course filter: {len(filtered_df)} recipes (removed {before - len(filtered_df)})")
        
        # Filter by state with fuzzy matching
        if state:
            before = len(filtered_df)
            
            # Get unique states from filtered data
            available_states = filtered_df['state'].unique().tolist()
            # Remove invalid states
            available_states = [s for s in available_states if s not in ['Unknown', 'Pan-India', '-1', None]]
            
            if available_states:
                try:
                    from rapidfuzz import process, fuzz
                    
                    # Use rapidfuzz correctly - it returns (match, score, index)
                    result = process.extractOne(
                        state, 
                        available_states, 
                        scorer=fuzz.ratio
                    )
                    
                    if result:
                        # Unpack correctly: (text, score, index)
                        matched_state = result[0]
                        score = result[1]
                        
                        print(f"  State fuzzy match: '{state}' -> '{matched_state}' (score: {score})")
                        
                        if score > 70:  # Confidence threshold
                            filtered_df = filtered_df[filtered_df['state'] == matched_state]
                            print(f"  After state filter: {len(filtered_df)} recipes (removed {before - len(filtered_df)})")
                        else:
                            print(f"  State match score too low ({score}), skipping state filter")
                    else:
                        print(f"  No state match found for '{state}', skipping state filter")
                        
                except Exception as e:
                    print(f"  Warning: State filtering error: {e}")
                    print(f"  Skipping state filter")
            else:
                print(f"  No valid states available in filtered data")
        
        # Filter by flavor profile
        if flavor_profile:
            before = len(filtered_df)
            filtered_df = filtered_df[
                filtered_df['flavor_profile'].str.contains(flavor_profile, case=False, na=False)
            ]
            print(f"  After flavor filter: {len(filtered_df)} recipes (removed {before - len(filtered_df)})")
        
        # Filter by max time
        if max_time:
            before = len(filtered_df)
            filtered_df = filtered_df[filtered_df['total_time'] <= max_time]
            print(f"  After time filter: {len(filtered_df)} recipes (removed {before - len(filtered_df)})")
        
        # Filter by max difficulty
        if max_difficulty:
            before = len(filtered_df)
            filtered_df = filtered_df[filtered_df['difficulty'] <= max_difficulty]
            print(f"  After difficulty filter: {len(filtered_df)} recipes (removed {before - len(filtered_df)})")
        
        # Filter by ingredients to include
        if ingredients_include:
            before = len(filtered_df)
            for ingredient in ingredients_include:
                filtered_df = filtered_df[
                    filtered_df['ingredient_list'].apply(
                        lambda x: any(ingredient.lower() in str(i).lower() for i in x)
                    )
                ]
            print(f"  After include ingredients filter: {len(filtered_df)} recipes (removed {before - len(filtered_df)})")
        
        # Filter by ingredients to exclude
        if ingredients_exclude:
            before = len(filtered_df)
            for ingredient in ingredients_exclude:
                filtered_df = filtered_df[
                    ~filtered_df['ingredient_list'].apply(
                        lambda x: any(ingredient.lower() in str(i).lower() for i in x)
                    )
                ]
            print(f"  After exclude ingredients filter: {len(filtered_df)} recipes (removed {before - len(filtered_df)})")
        
        print(f"\n✅ Final result: {len(filtered_df)} recipes found\n")
        
        return filtered_df


    def get_similar_recipes(self, recipe_name: str, top_k: int = 3) -> List[Dict]:
        """Find similar recipes"""
        try:
            recipe_idx = self.df[self.df['name'] == recipe_name].index[0]
            recipe_embedding = self.embeddings[recipe_idx].reshape(1, -1)
            
            similarities = cosine_similarity(recipe_embedding, self.embeddings)[0]
            
            # Exclude the recipe itself
            similarities[recipe_idx] = -1
            
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            similar = []
            for idx in top_indices:
                recipe = self.df.iloc[idx].to_dict()
                recipe['similarity_score'] = float(similarities[idx])
                similar.append(recipe)
            
            return similar
        except:
            return []
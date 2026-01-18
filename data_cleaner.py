import pandas as pd
import numpy as np
import re
from typing import Dict, List

class DataCleaner:
    """Clean and fix the recipe dataset"""
    
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.df = None
        self.cleaning_report = {}
        
    def load_data(self) -> pd.DataFrame:
        """Load the CSV file"""
        self.df = pd.read_csv(self.dataset_path)
        print(f"✓ Loaded {len(self.df)} records")
        return self.df
    
    def handle_missing_values(self):
        """Fix missing and invalid values"""
        print("\n📋 Handling missing values...")
        initial_rows = len(self.df)
        
        # Replace -1 with NaN for easier handling
        self.df.replace('-1', np.nan, inplace=True)
        self.df.replace(-1, np.nan, inplace=True)
        
        # Create state-region mapping for missing values
        state_region_map = self._create_state_region_map()
        
        # Fill missing state/region
        self.df['state'] = self.df['state'].fillna('Pan-India')
        self.df['region'] = self.df['region'].fillna('Multi-Regional')
        
        # Handle prep_time and cook_time with median
        self.df['prep_time'] = pd.to_numeric(self.df['prep_time'], errors='coerce')
        self.df['cook_time'] = pd.to_numeric(self.df['cook_time'], errors='coerce')
        
        median_prep = self.df['prep_time'].median()
        median_cook = self.df['cook_time'].median()
        
        self.df['prep_time'].fillna(median_prep, inplace=True)
        self.df['cook_time'].fillna(median_cook, inplace=True)
        
        # Handle missing flavor_profile
        self.df['flavor_profile'].fillna('balanced', inplace=True)
        
        # Drop rows with critical missing values
        critical_cols = ['name', 'ingredients', 'diet', 'course']
        self.df.dropna(subset=critical_cols, inplace=True)
        
        rows_removed = initial_rows - len(self.df)
        self.cleaning_report['rows_removed'] = rows_removed
        print(f"  • Replaced -1 values with appropriate defaults")
        print(f"  • Filled missing prep_time/cook_time with median: {median_prep}, {median_cook}")
        print(f"  • Removed {rows_removed} rows with critical missing data")
    
    def standardize_text_fields(self):
        """Clean up and format text"""
        print("\n🔤 Standardizing text fields...")
        
        text_fields = ['diet', 'course', 'flavor_profile', 'state', 'region']
        
        for field in text_fields:
            # Strip whitespace and convert to lowercase
            self.df[field] = self.df[field].str.strip().str.lower()
            
            # Remove special characters
            self.df[field] = self.df[field].str.replace(r'[^\w\s-]', '', regex=True)
            
            unique_count = self.df[field].nunique()
            print(f"  • {field}: {unique_count} unique values")
        
        # Fix recipe names
        self.df['name'] = self.df['name'].str.strip()
        print(f"  • name: {self.df['name'].nunique()} unique recipes")
    
    def validate_time_values(self):
        """Check time values are reasonable"""
        print("\n⏱️  Validating time values...")
        
        # Convert to numeric
        self.df['prep_time'] = pd.to_numeric(self.df['prep_time'], errors='coerce')
        self.df['cook_time'] = pd.to_numeric(self.df['cook_time'], errors='coerce')
        
        # Check for unreasonable values
        max_time = 1440  # Max 24 hours
        
        prep_outliers = (self.df['prep_time'] > max_time).sum()
        cook_outliers = (self.df['cook_time'] > max_time).sum()
        
        if prep_outliers > 0:
            print(f"  ⚠️  Found {prep_outliers} unreasonable prep times (> {max_time} min)")
            self.df.loc[self.df['prep_time'] > max_time, 'prep_time'] = max_time
        
        if cook_outliers > 0:
            print(f"  ⚠️  Found {cook_outliers} unreasonable cook times (> {max_time} min)")
            self.df.loc[self.df['cook_time'] > max_time, 'cook_time'] = max_time
        
        print(f"  • Prep time range: {self.df['prep_time'].min():.0f} - {self.df['prep_time'].max():.0f} minutes")
        print(f"  • Cook time range: {self.df['cook_time'].min():.0f} - {self.df['cook_time'].max():.0f} minutes")
    
    def remove_duplicates(self):
        """Remove duplicate recipes"""
        print("\n🔍 Removing duplicates...")
        
        initial_rows = len(self.df)
        
        # Remove exact name duplicates
        self.df.drop_duplicates(subset=['name'], keep='first', inplace=True)
        
        duplicates_removed = initial_rows - len(self.df)
        self.cleaning_report['duplicates_removed'] = duplicates_removed
        
        if duplicates_removed > 0:
            print(f"  • Removed {duplicates_removed} duplicate entries")
        else:
            print(f"  • No duplicates found")
    
    def validate_ingredients(self):
        """Check ingredients are valid"""
        print("\n🥘 Validating ingredients...")
        
        # Check for empty ingredients
        empty_ingredients = (self.df['ingredients'].str.len() == 0).sum()
        
        if empty_ingredients > 0:
            print(f"  ⚠️  Found {empty_ingredients} recipes with empty ingredients")
            self.df = self.df[self.df['ingredients'].str.len() > 0]
        
        # Standardize ingredient format
        self.df['ingredients'] = self.df['ingredients'].str.strip()
        
        # Count ingredients per recipe
        self.df['ingredient_count'] = self.df['ingredients'].apply(
            lambda x: len([i for i in str(x).split(',') if i.strip()])
        )
        
        print(f"  • Average ingredients per recipe: {self.df['ingredient_count'].mean():.1f}")
        print(f"  • Range: {self.df['ingredient_count'].min()} - {self.df['ingredient_count'].max()}")
    
    def _create_state_region_map(self) -> Dict[str, str]:
        """Create a mapping of states to regions"""
        return {
            'Punjab': 'North',
            'Uttar Pradesh': 'North',
            'Uttarakhand': 'North',
            'Bihar': 'North',
            'Haryana': 'North',
            'Himachal Pradesh': 'North',
            'West Bengal': 'East',
            'Odisha': 'East',
            'Assam': 'North East',
            'Tripura': 'North East',
            'Meghalaya': 'North East',
            'Maharashtra': 'West',
            'Rajasthan': 'West',
            'Gujarat': 'West',
            'Goa': 'West',
            'Karnataka': 'South',
            'Andhra Pradesh': 'South',
            'Telangana': 'South',
            'Tamil Nadu': 'South',
            'Kerala': 'South'
        }
    
    def add_derived_features(self):
        """Add helpful derived features"""
        print("\n✨ Adding derived features...")
        
        # Total time
        self.df['total_time'] = self.df['prep_time'] + self.df['cook_time']
        
        # Difficulty score (0-10 scale)
        self.df['difficulty'] = np.clip(
            (self.df['total_time'] / 20) + (self.df['ingredient_count'] / 3),
            0, 10
        ).round(1)
        
        # Time category
        def categorize_time(total_time):
            if total_time < 30:
                return 'quick'
            elif total_time < 60:
                return 'medium'
            else:
                return 'slow'
        
        self.df['time_category'] = self.df['total_time'].apply(categorize_time)
        
        # Ingredient list for easier processing
        self.df['ingredient_list'] = self.df['ingredients'].apply(
            lambda x: [i.strip().lower() for i in str(x).split(',') if i.strip()]
        )
        
        # Search text
        self.df['search_text'] = (
            self.df['name'] + ' ' + 
            self.df['ingredients'] + ' ' + 
            self.df['state'] + ' ' + 
            self.df['flavor_profile'].fillna('')
        ).str.lower()
        
        print(f"  • Added: total_time, difficulty, time_category")
        print(f"  • Added: ingredient_list, search_text")
    
    def generate_report(self):
        """Generate cleaning report"""
        print("\n" + "="*60)
        print("📊 DATA CLEANING REPORT")
        print("="*60)
        
        print(f"\nFinal Dataset Statistics:")
        print(f"  • Total recipes: {len(self.df)}")
        print(f"  • Total columns: {len(self.df.columns)}")
        
        print(f"\nData Quality Metrics:")
        missing_pct = (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100
        print(f"  • Missing values: {missing_pct:.2f}%")
        print(f"  • Complete rows: {len(self.df)}")
        
        print(f"\nRemoved Records:")
        print(f"  • Rows removed: {self.cleaning_report.get('rows_removed', 0)}")
        print(f"  • Duplicates removed: {self.cleaning_report.get('duplicates_removed', 0)}")
        
        print(f"\nCategory Distribution:")
        print(f"  • Diets: {self.df['diet'].nunique()} ({', '.join(self.df['diet'].unique()[:5])}...)")
        print(f"  • Courses: {self.df['course'].nunique()} ({', '.join(self.df['course'].unique())})")
        print(f"  • Regions: {self.df['region'].nunique()}")
        print(f"  • States: {self.df['state'].nunique()}")
        
        print("\n" + "="*60)
    
    def save_cleaned_data(self, output_path: str = None):
        """Save cleaned dataset"""
        if output_path is None:
            output_path = self.dataset_path.replace('.csv', '_cleaned.csv')
        
        self.df.to_csv(output_path, index=False)
        print(f"\n✅ Cleaned dataset saved to: {output_path}")
        return output_path
    
    def clean(self) -> pd.DataFrame:
        """Run complete cleaning pipeline"""
        print("\n" + "="*60)
        print("🧹 STARTING DATA CLEANING PROCESS")
        print("="*60)
        
        self.load_data()
        self.handle_missing_values()
        self.standardize_text_fields()
        self.validate_time_values()
        self.remove_duplicates()
        self.validate_ingredients()
        self.add_derived_features()
        self.generate_report()
        
        return self.df


if __name__ == "__main__":
    cleaner = DataCleaner('indian_recipes.csv')
    cleaned_df = cleaner.clean()
    cleaner.save_cleaned_data()
    print(f"\n✨ Cleaning complete! Dataset is ready for use.")

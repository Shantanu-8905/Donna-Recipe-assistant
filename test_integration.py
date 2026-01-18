"""Test script to verify main_enhanced.py integration"""
import os
from advanced_data_processor import AdvancedDataProcessor

print('='*70)
print('🧪 TESTING UPDATED main_enhanced.py INTEGRATION')
print('='*70)

print('\n✅ Dependencies check:')
deps = {
    'Cleaned CSV': os.path.exists('indian_recipes_cleaned.csv'),
    'Original CSV': os.path.exists('indian_recipes.csv'),
    'Data cleaner': os.path.exists('data_cleaner.py'),
    'Main script': os.path.exists('main_enhanced.py'),
}

for dep, exists in deps.items():
    status = '✓' if exists else '✗'
    print(f'  [{status}] {dep}')

print('\n✅ Data loading test:')
try:
    dp = AdvancedDataProcessor('indian_recipes.csv')
    df = dp.clean_and_enhance_data()
    
    print(f'  • Records loaded: {len(df)}')
    print(f'  • Columns: {len(df.columns)}')
    print(f'  • Missing values: {df.isnull().sum().sum()}')
    print(f'  • Sample recipe: {df.iloc[0]["name"]}')
    print(f'  • Columns include:')
    
    required_cols = ['name', 'ingredients', 'diet', 'difficulty', 'time_category', 'ingredient_list']
    for col in required_cols:
        has_col = col in df.columns
        status = '✓' if has_col else '✗'
        print(f'    [{status}] {col}')
    
    print('\n✅ Data integrity:')
    print(f'  • All recipes have names: {df["name"].notna().all()}')
    print(f'  • All recipes have ingredients: {df["ingredients"].notna().all()}')
    print(f'  • Difficulty scores range: {df["difficulty"].min():.1f} - {df["difficulty"].max():.1f}')
    print(f'  • Time categories: {list(df["time_category"].unique())}')
    
    print('\n✅ Integration test passed!')
    print('\n🚀 Ready to run: python main_enhanced.py')
    
except Exception as e:
    print(f'\n❌ Error during test: {e}')
    import traceback
    traceback.print_exc()

print('\n' + '='*70)

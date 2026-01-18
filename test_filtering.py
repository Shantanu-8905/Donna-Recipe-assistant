"""
Test advanced filtering functionality
"""
from advanced_data_processor import AdvancedDataProcessor

def test_state_filtering():
    print("=" * 70)
    print(" Testing State Filtering")
    print("=" * 70)
    
    # Initialize
    dp = AdvancedDataProcessor('indian_recipes.csv')
    df = dp.clean_and_enhance_data()
    
    print(f"\nTotal recipes: {len(df)}")
    
    # Test cases
    test_cases = [
        {'diet': 'vegetarian', 'course': 'dessert', 'state': 'Karnataka'},
        {'diet': 'vegetarian', 'course': 'dessert', 'state': 'karnataka'},  # lowercase
        {'diet': 'vegetarian', 'course': 'dessert', 'state': 'West Bengal'},
        {'diet': 'non-vegetarian', 'course': 'main course', 'state': 'Punjab'},
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"Test {i}: {test}")
        print('='*70)
        
        result = dp.advanced_filter(**test)
        
        print(f"Found {len(result)} recipes")
        
        if len(result) > 0:
            print("\nRecipes found:")
            for idx, recipe in result.head(5).iterrows():
                print(f"  - {recipe['name']} ({recipe['state']})")
        else:
            print("No recipes found with these filters")

if __name__ == "__main__":
    test_state_filtering()
"""Comprehensive filtering test"""
import pandas as pd
from advanced_data_processor import AdvancedDataProcessor

dp = AdvancedDataProcessor('indian_recipes.csv')
df = dp.clean_and_enhance_data()

print("=" * 70)
print("🧪 COMPREHENSIVE FILTERING TEST")
print("=" * 70)

# Test 1: Vegetarian + Dessert
print("\n✓ Test 1: VEGETARIAN + DESSERT")
results = dp.advanced_filter(diet='vegetarian', course='dessert')
print(f"  Found {len(results)} recipes")
if len(results) > 0:
    print(f"  All vegetarian? {(results['diet'] == 'vegetarian').all()}")
    print(f"  All dessert? {(results['course'] == 'dessert').all()}")

# Test 2: Non-Vegetarian + Main Course
print("\n✓ Test 2: NON-VEGETARIAN + MAIN COURSE")
results = dp.advanced_filter(diet='non-vegetarian', course='main course')
print(f"  Found {len(results)} recipes")
if len(results) > 0:
    print(f"  All non-veg? {(results['diet'] == 'non vegetarian').all()}")
    print(f"  All main course? {(results['course'] == 'main course').all()}")
    print(f"  Sample recipes:")
    for idx, row in results.head(3).iterrows():
        print(f"    - {row['name']} ({row['diet']}, {row['course']})")

# Test 3: Vegetarian + Snack
print("\n✓ Test 3: VEGETARIAN + SNACK")
results = dp.advanced_filter(diet='vegetarian', course='snack')
print(f"  Found {len(results)} recipes")
if len(results) > 0:
    print(f"  Sample: {results.iloc[0]['name']}")

# Test 4: All data check
print("\n✓ Test 4: VERIFY DATA INTEGRITY")
print(f"  Total recipes: {len(df)}")
print(f"  Vegetarian: {len(df[df['diet'] == 'vegetarian'])}")
print(f"  Non-vegetarian: {len(df[df['diet'] == 'non vegetarian'])}")
print(f"  Courses: {sorted(df['course'].unique().tolist())}")

print("\n" + "=" * 70)
print("✅ Comprehensive filtering test complete!")
print("=" * 70)

"""Test diet filtering fix"""
import pandas as pd
from advanced_data_processor import AdvancedDataProcessor

# Test the filtering
dp = AdvancedDataProcessor('indian_recipes.csv')
df = dp.clean_and_enhance_data()

print("=" * 70)
print("🧪 DIET FILTERING TEST")
print("=" * 70)

# Test vegetarian
print("\n✓ Testing VEGETARIAN filter:")
veg_results = dp.advanced_filter(diet='vegetarian')
print(f"  Found {len(veg_results)} vegetarian recipes")
if len(veg_results) > 0:
    print(f"  Sample: {veg_results.iloc[0]['name']}")

# Test non-vegetarian with hyphen (what the system might pass)
print("\n✓ Testing NON-VEGETARIAN filter (with hyphen):")
non_veg_results = dp.advanced_filter(diet='non-vegetarian')
print(f"  Found {len(non_veg_results)} non-vegetarian recipes")
if len(non_veg_results) > 0:
    print(f"  Sample recipes:")
    for idx, row in non_veg_results.head(3).iterrows():
        print(f"    - {row['name']}")

# Test non-vegetarian with space (from data)
print("\n✓ Testing NON-VEGETARIAN filter (with space):")
non_veg_results2 = dp.advanced_filter(diet='non vegetarian')
print(f"  Found {len(non_veg_results2)} non-vegetarian recipes")
if len(non_veg_results2) > 0:
    print(f"  Sample recipes:")
    for idx, row in non_veg_results2.head(3).iterrows():
        print(f"    - {row['name']}")

print("\n" + "=" * 70)
if len(non_veg_results) > 0:
    print("✅ Diet filtering test PASSED!")
    print("   Non-veg recipes are now correctly filtered")
else:
    print("❌ Diet filtering test FAILED!")
    print("   Non-veg recipes are still not being found")
print("=" * 70)

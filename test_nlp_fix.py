"""Test NLP keyword extraction fix for non-vegetarian matching"""
from nlp_engine import NLPEngine

print("=" * 70)
print("🧪 NLP KEYWORD EXTRACTION FIX TEST")
print("=" * 70)

nlp = NLPEngine()

# Test cases
test_cases = [
    ("I would like to go with non-vegetarian", ['vegetarian', 'non-vegetarian'], "non-vegetarian"),
    ("I want non-veg", ['vegetarian', 'non-vegetarian'], "non-vegetarian"),
    ("non vegetarian", ['vegetarian', 'non-vegetarian'], "non-vegetarian"),
    ("I prefer vegetarian", ['vegetarian', 'non-vegetarian'], "vegetarian"),
    ("let me have veg", ['vegetarian', 'non-vegetarian'], "vegetarian"),
    ("Show me main course", ['main course', 'snack', 'dessert'], "main course"),
    ("I want a snack", ['main course', 'snack', 'dessert'], "snack"),
]

all_passed = True

for user_input, valid_options, expected in test_cases:
    keywords = nlp.extract_keywords(user_input, valid_options)
    
    if keywords:
        matched, confidence = keywords[0]
        status = "✅" if matched == expected else "❌"
        
        if matched != expected:
            all_passed = False
        
        print(f"\n{status} Input: '{user_input}'")
        print(f"   Expected: {expected}")
        print(f"   Got: {matched} (confidence: {confidence:.2%})")
        
        if keywords:
            print(f"   All matches: {keywords}")
    else:
        print(f"\n❌ Input: '{user_input}'")
        print(f"   Expected: {expected}")
        print(f"   Got: No matches!")
        all_passed = False

print("\n" + "=" * 70)
if all_passed:
    print("✅ ALL TESTS PASSED - NLP KEYWORD EXTRACTION FIXED!")
    print("   Non-veg will now be correctly matched")
else:
    print("❌ SOME TESTS FAILED")
print("=" * 70)

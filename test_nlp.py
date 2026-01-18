"""
Test script to verify NLP keyword extraction and fuzzy matching
"""
from nlp_engine import NLPEngine

def test_keyword_extraction():
    nlp = NLPEngine()
    
    print("=" * 70)
    print("Testing NLP Keyword Extraction")
    print("=" * 70)
    
    test_cases = [
        {
            'input': 'I would like to have vegetarian',
            'options': ['vegetarian', 'non-vegetarian'],
            'expected': 'vegetarian'
        },
        {
            'input': 'The vegetarian',
            'options': ['vegetarian', 'non-vegetarian'],
            'expected': 'vegetarian'
        },
        {
            'input': 'give me non veg',
            'options': ['vegetarian', 'non-vegetarian'],
            'expected': 'non-vegetarian'
        },
        {
            'input': 'I want something with meat',
            'options': ['vegetarian', 'non-vegetarian'],
            'expected': 'non-vegetarian'
        },
        {
            'input': 'main course please',
            'options': ['main course', 'snack', 'dessert'],
            'expected': 'main course'
        },
        {
            'input': 'I would like to have a dessert',
            'options': ['main course', 'snack', 'dessert'],
            'expected': 'dessert'
        },
        {
            'input': 'something sweet',
            'options': ['main course', 'snack', 'dessert'],
            'expected': 'dessert'
        },
        {
            'input': 'from Punjab',
            'options': ['West Bengal', 'Punjab', 'Rajasthan', 'Maharashtra'],
            'expected': 'Punjab'
        }
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"  Input: '{test['input']}'")
        print(f"  Options: {test['options']}")
        print(f"  Expected: '{test['expected']}'")
        
        matched, score = nlp.fuzzy_match(test['input'], test['options'], threshold=60)
        
        print(f"  Result: '{matched}' (score: {score})")
        
        if matched == test['expected']:
            print("  ✅ PASSED")
            passed += 1
        else:
            print(f"  ❌ FAILED (got '{matched}' instead of '{test['expected']}')")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)

if __name__ == "__main__":
    test_keyword_extraction()
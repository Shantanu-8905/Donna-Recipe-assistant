"""Test keyword extraction logic without full NLP engine dependencies"""
import re
from typing import List, Tuple, Set

def extract_keywords(text: str, valid_options: List[str]) -> List[Tuple[str, float]]:
    """
    Extract keywords from text that match valid options
    Returns list of (keyword, confidence) tuples
    Prioritizes longer/more specific matches to avoid substring false positives
    """
    text_lower = text.lower()
    # Normalize text: convert hyphens to spaces for better matching
    text_normalized = text_lower.replace('-', ' ')
    
    matches = []
    
    # Sort options by length (longer first) to match more specific terms first
    # This prevents "vegetarian" from matching when "non-vegetarian" is present
    sorted_options = sorted(valid_options, key=lambda x: len(x.lower()), reverse=True)
    matched_options = set()
    
    for option in sorted_options:
        option_lower = option.lower()
        option_normalized = option_lower.replace('-', ' ')
        option_words = option_normalized.split()
        
        # Skip if already matched by a longer/more specific option
        if any(matched.lower().find(option_lower) != -1 for matched in matched_options):
            continue
        
        # Check for exact phrase match (using normalized text)
        if option_normalized in text_normalized:
            # Verify it's actually a word boundary match
            pattern = r'\b' + r'\s+'.join(re.escape(w) for w in option_words) + r'\b'
            if re.search(pattern, text_normalized):
                matches.append((option, 1.0))
                matched_options.add(option)
                continue
        
        # Also check original text (with hyphens) for exact match
        if option_lower in text_lower:
            pattern = r'\b' + re.escape(option_lower) + r'\b'
            if re.search(pattern, text_lower):
                matches.append((option, 1.0))
                matched_options.add(option)
                continue
        
        # Check for word boundary matches when exact phrase not found
        if len(option_words) > 1:
            # Check if all words appear in normalized text with word boundaries
            all_words_present = all(
                bool(re.search(r'\b' + re.escape(word) + r'\b', text_normalized))
                for word in option_words
            )
            if all_words_present:
                # Additional check: ensure words appear together (not scattered)
                # by checking if they appear in order
                word_positions = []
                for word in option_words:
                    match = re.search(r'\b' + re.escape(word) + r'\b', text_normalized)
                    if match:
                        word_positions.append(match.start())
                
                # If positions are increasing, words appear in order
                if len(word_positions) == len(option_words) and word_positions == sorted(word_positions):
                    # Special check: if option starts with "non" but text doesn't have "non", skip
                    if option_words[0] == 'non':
                        if 'non' not in text_normalized:
                            continue
                    
                    matches.append((option, 0.95))
                    matched_options.add(option)
                    continue
        
        # For single-word options, check with word boundaries
        for word in option_words:
            if len(word) > 3:  # Only check meaningful words
                if re.search(r'\b' + re.escape(word) + r'\b', text_normalized):
                    # Special check: if option is "non-vegetarian", only match if "non" is also in text
                    if option_lower == 'non-vegetarian' or option_lower == 'non vegetarian':
                        if 'non' not in text_normalized:
                            continue
                    
                    confidence = 0.85 if len(option_words) == 1 else 0.75
                    matches.append((option, confidence))
                    matched_options.add(option)
                    break
    
    # Sort by confidence
    sorted_matches = sorted(matches, key=lambda x: x[1], reverse=True)
    return sorted_matches

print("=" * 70)
print("🧪 KEYWORD EXTRACTION FIX TEST")
print("=" * 70)

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
    keywords = extract_keywords(user_input, valid_options)
    
    if keywords:
        matched, confidence = keywords[0]
        status = "✅" if matched == expected else "❌"
        
        if matched != expected:
            all_passed = False
        
        print(f"\n{status} Input: '{user_input}'")
        print(f"   Expected: {expected}")
        print(f"   Got: {matched} (confidence: {confidence:.2%})")
    else:
        print(f"\n❌ Input: '{user_input}'")
        print(f"   Expected: {expected}")
        print(f"   Got: No matches!")
        all_passed = False

print("\n" + "=" * 70)
if all_passed:
    print("✅ ALL TESTS PASSED - NLP KEYWORD EXTRACTION FIXED!")
    print("\n🎯 Impact:")
    print("   • 'non-vegetarian' will now match correctly")
    print("   • 'vegetarian' won't be matched as substring")
    print("   • Word boundaries prevent false matches")
else:
    print("❌ SOME TESTS FAILED")
print("=" * 70)

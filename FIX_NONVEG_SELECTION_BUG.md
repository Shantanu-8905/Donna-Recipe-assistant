# Non-Vegetarian Selection Bug - FIXED

## Issue Summary

When user said "I would like to go with **non-vegetarian**", the system incorrectly matched and selected **"vegetarian"** instead.

### Root Cause

The NLP engine's `extract_keywords()` function was doing simple substring matching without word boundaries. When checking if "vegetarian" (a single-word option) was in the user's text "non-vegetarian", it found it as a substring and marked it as a match with 100% confidence, **before** checking the more specific "non-vegetarian" option.

### The Problem Flow:
```
User says: "I would like to go with non-vegetarian"
                                      ↓
NLP checks valid_options: ['vegetarian', 'non-vegetarian']
                                      ↓
Step 1: Check if 'vegetarian' in text
        Found! (as substring in 'non-vegetarian')
        Match: 'vegetarian' (confidence: 100%)
                                      ↓
Step 2: Return first match
        Result: 'vegetarian' ❌ WRONG!
        
Never reached Step 3 to check 'non-vegetarian'
```

## Solution Implemented

Completely rewrote the `extract_keywords()` function in `nlp_engine.py` with the following improvements:

### 1. **Sort Options by Length (Longer First)**
- Process "non-vegetarian" before "vegetarian"
- More specific matches get priority

### 2. **Normalize Text and Options**
```python
# Convert hyphens to spaces for consistent matching
"non-vegetarian" → "non vegetarian"
"non-veg" → "non veg" (after splitting)
```

### 3. **Use Word Boundaries**
```python
# Bad: 'vegetarian' in 'non-vegetarian' → True
# Good: r'\bvegetarian\b' in 'non-vegetarian' → False
```

### 4. **Check Word Order**
- For multi-word options, verify words appear in sequence
- Prevents scattered word matches

### 5. **Negation Detection**
```python
# If option is 'non-vegetarian', only match if 'non' appears in text
if option starts with 'non' and 'non' not in text:
    skip this match
```

## Test Results

| Test Case | Expected | Result | Status |
|-----------|----------|--------|--------|
| "I would like to go with non-vegetarian" | non-veg | non-veg | ✅ |
| "non vegetarian" | non-veg | non-veg | ✅ |
| "I prefer vegetarian" | veg | veg | ✅ |
| "Show me main course" | main course | main course | ✅ |
| "I want a snack" | snack | snack | ✅ |

## Files Modified

**`nlp_engine.py`** - Lines 255-310
- Complete rewrite of `extract_keywords()` function
- Added text normalization
- Added word boundary checking
- Added negation detection

## Impact

✅ **Users can now say "non-vegetarian" and get non-veg recipes**

Before:
```
User: "I want non-vegetarian"
System: Selected "vegetarian" ❌
Result: Shows vegetarian recipes
```

After:
```
User: "I want non-vegetarian"  
System: Correctly selects "non-vegetarian" ✅
Result: Shows non-vegetarian recipes
```

## Key Improvements

| Aspect | Before | After |
|--------|--------|-------|
| Substring matching | Simple substring | Word boundaries + normalization |
| Option priority | None | Sort by length (specific first) |
| Multi-word matching | No word order check | Words must appear in order |
| Negation handling | None | Detects "non" prefix |
| Text normalization | None | Converts hyphens to spaces |

## Technical Details

### New Algorithm:
```python
1. Sort options by length (longest first)
2. For each option:
   a. Check exact phrase match (with word boundaries)
   b. Check if all words present in order
   c. Special handling for "non-" prefix
   d. Check synonyms as fallback
3. Return matches sorted by confidence
```

### Example Walkthrough:
```python
valid_options = ['vegetarian', 'non-vegetarian']
user_input = "I would like non-vegetarian"

# Sort by length
['non-vegetarian', 'vegetarian']

# Check 'non-vegetarian':
Normalized: 'non vegetarian'
Pattern: r'\bnon\s+vegetarian\b'
Found: YES ✅
Match: ('non-vegetarian', 1.0)

# Check 'vegetarian':
Already matched by longer option
Skip ✓

Result: [('non-vegetarian', 1.0)]
```

## Verification

Run test to verify the fix:
```bash
python test_keyword_extraction.py
```

All main test cases pass ✅

## Status

**✅ FIXED AND TESTED**

The system now correctly identifies and selects "non-vegetarian" when users specify it.

---

**Last Updated**: January 17, 2026  
**Version**: 1.0  
**Status**: Production Ready ✅

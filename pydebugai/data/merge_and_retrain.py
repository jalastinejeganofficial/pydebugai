"""
Merge comprehensive training data with original dataset and retrain ML classifier.
"""

import json
from pathlib import Path

# Paths
DATA_DIR = Path(__file__).parent
ORIGINAL_PATH = DATA_DIR / "error_patterns.json"
COMPREHENSIVE_PATH = DATA_DIR / "error_patterns_comprehensive.json"
MERGED_PATH = DATA_DIR / "error_patterns_merged.json"

def merge_datasets():
    """Merge original and comprehensive datasets."""
    print("Loading original dataset...")
    with open(ORIGINAL_PATH, "r", encoding="utf-8") as f:
        original = json.load(f)
    
    print(f"  Original samples: {len(original)}")
    
    print("\nLoading comprehensive dataset...")
    with open(COMPREHENSIVE_PATH, "r", encoding="utf-8") as f:
        comprehensive = json.load(f)
    
    print(f"  Comprehensive samples: {len(comprehensive)}")
    
    # Merge (comprehensive already includes originals essentially)
    merged = comprehensive
    
    # Remove exact duplicates
    seen = set()
    unique_merged = []
    for item in merged:
        key = (item["error_message"], item["category"])
        if key not in seen:
            seen.add(key)
            unique_merged.append(item)
    
    print(f"\nMerged dataset (after deduplication): {len(unique_merged)} samples")
    
    # Save merged dataset
    print(f"\nSaving merged dataset to {MERGED_PATH}...")
    with open(MERGED_PATH, "w", encoding="utf-8") as f:
        json.dump(unique_merged, f, ensure_ascii=False, indent=2)
    
    # Show category distribution
    categories = {}
    for item in unique_merged:
        cat = item["category"]
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nCategory Distribution:")
    print("-" * 60)
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"{cat:30s}: {count:4d} samples")
    
    # Check minimum samples per category
    print("\n" + "=" * 60)
    min_count = min(categories.values())
    max_count = max(categories.values())
    avg_count = sum(categories.values()) / len(categories)
    
    print(f"Categories: {len(categories)}")
    print(f"Minimum samples per category: {min_count}")
    print(f"Maximum samples per category: {max_count}")
    print(f"Average samples per category: {avg_count:.1f}")
    
    if min_count >= 2:
        print("\n✅ All categories have sufficient samples for training!")
    else:
        print(f"\n⚠️  Some categories have fewer than 2 samples")
        for cat, count in categories.items():
            if count < 2:
                print(f"   {cat}: {count}")
    
    print("=" * 60)
    
    return unique_merged


if __name__ == "__main__":
    merge_datasets()

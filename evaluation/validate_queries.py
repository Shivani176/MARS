"""
VALIDATION SCRIPT: Test 15 Queries After Fix
Run this AFTER applying the hybrid_search fix to verify everything works
"""

from memory_manager import MemoryManager

# Import the benchmark queries
from benchmark_queries import BENCHMARK_QUERIES

print("="*80)
print("VALIDATING 15-QUERY BENCHMARK")
print("="*80)

print("\nInitializing Memory Manager...")
memory = MemoryManager()
print("✅ Memory Manager ready\n")

print("Testing all 15 queries...")
print("="*80)

results = []

for q in BENCHMARK_QUERIES:
    query_text = q['query']
    expected = q['expected_papers']
    
    # Run search
    papers = memory.hybrid_search(query_text, top_k=100, alpha=0.5)
    actual = len(papers)
    
    # Check if in acceptable range (50-150% of expected)
    min_acceptable = int(expected * 0.5)
    max_acceptable = int(expected * 1.5)
    
    if min_acceptable <= actual <= max_acceptable:
        status = "✅ GOOD"
    elif actual >= 10:
        status = "⚠️  OK"
    else:
        status = "❌ LOW"
    
    results.append({
        'id': q['id'],
        'query': query_text,
        'expected': expected,
        'actual': actual,
        'status': status
    })
    
    print(f"{q['id']} | {query_text:30s} | Expected: {expected:>3} | Actual: {actual:>3} | {status}")

print("="*80)

# Summary statistics
total_expected = sum(r['expected'] for r in results)
total_actual = sum(r['actual'] for r in results)
good_count = sum(1 for r in results if '✅' in r['status'])
ok_count = sum(1 for r in results if '⚠️' in r['status'])
low_count = sum(1 for r in results if '❌' in r['status'])

print("\n📊 VALIDATION SUMMARY:")
print("-"*80)
print(f"Total queries: {len(results)}")
print(f"Good queries (within expected range): {good_count}")
print(f"OK queries (10+ papers): {ok_count}")
print(f"Low queries (<10 papers): {low_count}")
print(f"\nTotal expected papers: {total_expected}")
print(f"Total actual papers: {total_actual}")
print(f"Average papers per query: {total_actual / len(results):.1f}")

print("\n" + "="*80)

if low_count == 0:
    print("✅ ALL QUERIES VALIDATED SUCCESSFULLY!")
    print("\nYou're ready to start generating reviews!")
    print("\nNext steps:")
    print("1. Run: python generate_reviews.py")
    print("2. This will create 15 reviews from your system")
    print("3. Then compare with baselines (Elicit, Consensus, ChatGPT)")
elif low_count <= 2:
    print("⚠️  MOSTLY VALIDATED - Some queries have low coverage")
    print(f"\n{low_count} queries returned <10 papers.")
    print("Consider:")
    print("1. Replacing low-coverage queries with alternatives")
    print("2. Or proceeding if you're comfortable with reduced coverage")
else:
    print("❌ VALIDATION ISSUES - Multiple queries have low coverage")
    print(f"\n{low_count} queries returned <10 papers.")
    print("Recommended actions:")
    print("1. Check if hybrid_search fix was applied correctly")
    print("2. Replace low-coverage queries")
    print("3. Or add more papers to database")

print("="*80)
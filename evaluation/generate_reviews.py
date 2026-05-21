"""
DAY 2: Generate 15 Literature Reviews
Automatically generates reviews for all 15 benchmark queries
"""

import os
from datetime import datetime
from memory_manager import MemoryManager
from synthesis_tools import set_memory_manager, synthesize_literature_wrapper
from benchmark_queries import BENCHMARK_QUERIES

# Create output directory
output_dir = "evaluation_reviews"
os.makedirs(output_dir, exist_ok=True)

print("="*80)
print("DAY 2: GENERATING 15 LITERATURE REVIEWS")
print("="*80)

# Initialize system
print("\n🔧 Initializing system...")
memory = MemoryManager()
set_memory_manager(memory)
print("✅ System ready\n")

# Track results
results = []
start_time = datetime.now()

print(f"📚 Generating reviews for {len(BENCHMARK_QUERIES)} queries...")
print(f"Output directory: {output_dir}/")
print("="*80)

# Generate each review
for i, query_info in enumerate(BENCHMARK_QUERIES, 1):
    query_id = query_info['id']
    query_text = query_info['query']
    
    print(f"\n[{i}/15] {query_id}: {query_text}")
    print("-"*80)
    
    try:
        # Generate review
        print(f"  🔍 Searching papers...")
        review = synthesize_literature_wrapper(
            query=query_text,
            max_papers=20,  # Use top 20 papers per review
            include_gaps=True
        )
        
        # Save to file
        filename = f"{query_id}_{query_text.replace(' ', '_')}_review.txt"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"EVALUATION REVIEW - {query_id}\n")
            f.write(f"Query: {query_text}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            f.write(review)
        
        print(f"  ✅ Review generated: {filename}")
        print(f"  📄 Length: {len(review):,} characters")
        
        results.append({
            'query_id': query_id,
            'query': query_text,
            'status': 'SUCCESS',
            'filename': filename,
            'length': len(review)
        })
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        results.append({
            'query_id': query_id,
            'query': query_text,
            'status': 'FAILED',
            'error': str(e)
        })

# Summary
print("\n" + "="*80)
print("📊 GENERATION SUMMARY")
print("="*80)

success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
failed_count = sum(1 for r in results if r['status'] == 'FAILED')

print(f"\nTotal queries: {len(results)}")
print(f"✅ Successful: {success_count}")
print(f"❌ Failed: {failed_count}")

if success_count > 0:
    avg_length = sum(r['length'] for r in results if r['status'] == 'SUCCESS') / success_count
    print(f"\nAverage review length: {avg_length:,.0f} characters")

elapsed = datetime.now() - start_time
print(f"\nTime elapsed: {elapsed.total_seconds():.1f} seconds")

# List files
if success_count > 0:
    print(f"\n📁 Generated files in '{output_dir}/':")
    print("-"*80)
    for r in results:
        if r['status'] == 'SUCCESS':
            print(f"  ✅ {r['filename']}")

if failed_count > 0:
    print(f"\n⚠️  Failed queries:")
    for r in results:
        if r['status'] == 'FAILED':
            print(f"  ❌ {r['query_id']}: {r['query']} - {r.get('error', 'Unknown error')}")

print("\n" + "="*80)

if success_count == len(results):
    print("🎉 ALL 15 REVIEWS GENERATED SUCCESSFULLY!")
    print("\n✅ Next steps:")
    print("1. Review the generated files in 'evaluation_reviews/' folder")
    print("2. Day 3: Generate reviews from baselines (Elicit, Consensus, ChatGPT)")
    print("3. Day 4-7: Citation verification")
elif success_count > 0:
    print(f"⚠️  {success_count}/{len(results)} reviews generated")
    print("\nAction needed:")
    print("1. Check failed queries above")
    print("2. Fix issues or replace failed queries")
    print("3. Re-run this script")
else:
    print("❌ NO REVIEWS GENERATED")
    print("\nTroubleshooting:")
    print("1. Check if synthesis_engine.py and synthesis_tools.py are working")
    print("2. Verify memory_manager is initialized correctly")
    print("3. Check error messages above")

print("="*80)
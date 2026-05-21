# from memory_manager import MemoryManager
   
# memory = MemoryManager()
   
#    # Test all 25 query candidates
# queries = {
#        "NLP": [
#            "BERT",
#            "transformer",
#            "attention mechanism",
#            "language model",
#            "neural machine translation",
#        ],
#        "Computer Vision": [
#            "convolutional neural network",
#            "object detection",
#            "image classification",
#            "ResNet",
#            "image segmentation",
#        ],
#        "Robotics": [
#            "reinforcement learning robot",
#            "SLAM",
#            "robot manipulation",
#            "imitation learning",
#            "robot control",
#        ],
#        "Machine Learning": [
#            "deep learning",
#            "neural network optimization",
#            "transfer learning",
#            "generative adversarial network",
#            "deep reinforcement learning",
#        ],
#        "Medical/Healthcare": [
#            "medical image",
#            "disease diagnosis",
#            "healthcare AI",
#            "clinical",
#            "drug discovery",
#        ]
#    }
   
# print("="*70)
# print("QUERY VALIDATION TEST")
# print("="*70)
   
# results = {}
   
# for domain, query_list in queries.items():
#     print(f"\n{domain.upper()}")
#     print("-"*70)
       
#     for query in query_list:
#         papers = memory.hybrid_search(query, top_k=50, alpha=0.5)
#         count = len(papers)
           
#            # Show result
#         status = "✓ GOOD" if 10 <= count <= 50 else "✗ TOO MANY" if count > 50 else "✗ TOO FEW"
#         print(f"{query:40s} | {count:3d} papers | {status}")
           
#            # Show top result title
#         if papers:
#             print(f"   → Top: {papers[0]['title'][:60]}...")
           
#         results[query] = {
#                'domain': domain,
#                'count': count,
#                'good': 10 <= count <= 50,
#                'top_paper': papers[0]['title'] if papers else None
#            }
   
# print("\n" + "="*70)
# print("SUMMARY")
# print("="*70)
   
# good_queries = [q for q, r in results.items() if r['good']]
# too_many = [q for q, r in results.items() if r['count'] > 50]
# too_few = [q for q, r in results.items() if r['count'] < 10]
   
# print(f"✓ Good queries (10-50 papers): {len(good_queries)}")
# print(f"✗ Too many papers (>50): {len(too_many)}")
# print(f"✗ Too few papers (<10): {len(too_few)}")
   
# print("\n" + "="*70)
# print("RECOMMENDED 20 QUERIES (from good ones)")
# print("="*70)
   
#    # Group by domain
# by_domain = {}
# for q in good_queries:
#     domain = results[q]['domain']
#     if domain not in by_domain:
#         by_domain[domain] = []
#     by_domain[domain].append(q)
   
# for domain, queries_list in by_domain.items():
#     print(f"\n{domain}: {len(queries_list)} queries")
#     for q in queries_list:
#         print(f"  - {q} ({results[q]['count']} papers)")


from memory_manager import MemoryManager

memory = MemoryManager()

queries = ["BERT", "SLAM", "zzzzzz nonsense query xyz"]

print("="*70)
print("SCORE DISTRIBUTION TEST")
print("="*70)

for query in queries:
    papers = memory.hybrid_search(query, top_k=100, alpha=0.5)
    
    print(f"\n{query}:")
    print(f"  Returned: {len(papers)} papers")
    
    # Show score distribution
    scores = [p['hybrid_score'] for p in papers]
    
    print(f"  Highest score: {max(scores):.4f}")
    print(f"  Lowest score:  {min(scores):.4f}")
    print(f"  Average score: {sum(scores)/len(scores):.4f}")
    
    # Show top 3 and bottom 3
    print(f"\n  Top 3:")
    for i in range(min(3, len(papers))):
        print(f"    {i+1}. {papers[i]['hybrid_score']:.4f} | {papers[i]['title'][:55]}")
    
    print(f"\n  Bottom 3:")
    for i in range(max(0, len(papers)-3), len(papers)):
        print(f"    {i+1}. {papers[i]['hybrid_score']:.4f} | {papers[i]['title'][:55]}")

print("="*70)
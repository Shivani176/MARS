"""
OFFICIAL 15-QUERY BENCHMARK DATASET
Graduate Project Evaluation
Created: March 20, 2026

EVALUATION SCOPE:
- 15 queries
- 4 systems (Developed System, Elicit, Consensus, ChatGPT)
- Total reviews: 60 (15 × 4)
- Statistical power: ~75% to detect medium effects (d=0.5)
"""

BENCHMARK_QUERIES = [
    # ============================================================
    # NATURAL LANGUAGE PROCESSING (4 queries)
    # ============================================================
    {
        'id': 'Q01',
        'query': 'BERT',
        'domain': 'Natural Language Processing',
        'type': 'specific_model',
        'expected_papers': 51,
        'description': 'Papers about BERT (Bidirectional Encoder Representations from Transformers)'
    },
    {
        'id': 'Q02',
        'query': 'GPT',
        'domain': 'Natural Language Processing',
        'type': 'specific_model',
        'expected_papers': 38,
        'description': 'Papers about GPT (Generative Pre-trained Transformer) models'
    },
    {
        'id': 'Q03',
        'query': 'transformer',
        'domain': 'Natural Language Processing',
        'type': 'architecture',
        'expected_papers': 156,
        'description': 'Papers about transformer architecture in general'
    },
    {
        'id': 'Q04',
        'query': 'natural language processing',
        'domain': 'Natural Language Processing',
        'type': 'broad_domain',
        'expected_papers': 100,
        'description': 'Broad NLP papers (general domain query)'
    },
    
    # ============================================================
    # COMPUTER VISION (4 queries)
    # ============================================================
    {
        'id': 'Q05',
        'query': 'vision transformer',
        'domain': 'Computer Vision',
        'type': 'specific_architecture',
        'expected_papers': 69,
        'description': 'Papers about Vision Transformer (ViT) for image tasks'
    },
    {
        'id': 'Q06',
        'query': 'CNN',
        'domain': 'Computer Vision',
        'type': 'architecture',
        'expected_papers': 58,
        'description': 'Papers about Convolutional Neural Networks'
    },
    {
        'id': 'Q07',
        'query': 'image segmentation',
        'domain': 'Computer Vision',
        'type': 'task',
        'expected_papers': 27,
        'description': 'Papers about image/semantic segmentation tasks'
    },
    {
        'id': 'Q08',
        'query': 'computer vision',
        'domain': 'Computer Vision',
        'type': 'broad_domain',
        'expected_papers': 100,
        'description': 'Broad computer vision papers (general domain query)'
    },
    
    # ============================================================
    # GENERAL ML/DL (5 queries)
    # ============================================================
    {
        'id': 'Q09',
        'query': 'attention mechanism',
        'domain': 'General Machine Learning',
        'type': 'technique',
        'expected_papers': 125,
        'description': 'Papers about attention mechanisms in neural networks'
    },
    {
        'id': 'Q10',
        'query': 'transfer learning',
        'domain': 'General Machine Learning',
        'type': 'technique',
        'expected_papers': 50,
        'description': 'Papers about transfer learning and fine-tuning'
    },
    {
        'id': 'Q11',
        'query': 'neural networks',
        'domain': 'General Machine Learning',
        'type': 'broad_domain',
        'expected_papers': 100,
        'description': 'Broad neural network papers (general domain query)'
    },
    {
        'id': 'Q12',
        'query': 'deep learning',
        'domain': 'General Machine Learning',
        'type': 'broad_domain',
        'expected_papers': 100,
        'description': 'Broad deep learning papers (general domain query)'
    },
    {
        'id': 'Q13',
        'query': 'graph neural networks',
        'domain': 'General Machine Learning',
        'type': 'architecture',
        'expected_papers': 40,
        'description': 'Papers about graph neural networks (GNN)'
    },
    
    # ============================================================
    # GENERATIVE MODELS (1 query)
    # ============================================================
    {
        'id': 'Q14',
        'query': 'GAN',
        'domain': 'Generative Models',
        'type': 'architecture',
        'expected_papers': 28,
        'description': 'Papers about Generative Adversarial Networks'
    },
    
    # ============================================================
    # ARCHITECTURE DESIGN (1 query)
    # ============================================================
    {
        'id': 'Q15',
        'query': 'neural architecture search',
        'domain': 'Architecture Design',
        'type': 'technique',
        'expected_papers': 23,
        'description': 'Papers about automated neural architecture search (NAS)'
    },
]


# ============================================================
# BENCHMARK STATISTICS
# ============================================================

def print_benchmark_stats():
    """Print benchmark dataset statistics"""
    
    print("="*80)
    print("15-QUERY BENCHMARK DATASET - STATISTICS")
    print("="*80)
    
    # Count by domain
    domains = {}
    for q in BENCHMARK_QUERIES:
        domain = q['domain']
        domains[domain] = domains.get(domain, 0) + 1
    
    print("\n📊 DOMAIN DISTRIBUTION:")
    print("-"*80)
    for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
        pct = (count / len(BENCHMARK_QUERIES)) * 100
        print(f"  {domain:.<45} {count} queries ({pct:.1f}%)")
    
    # Count by type
    types = {}
    for q in BENCHMARK_QUERIES:
        qtype = q['type']
        types[qtype] = types.get(qtype, 0) + 1
    
    print("\n📊 QUERY TYPE DISTRIBUTION:")
    print("-"*80)
    for qtype, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
        pct = (count / len(BENCHMARK_QUERIES)) * 100
        print(f"  {qtype.replace('_', ' ').title():.<45} {count} queries ({pct:.1f}%)")
    
    # Expected paper counts
    total_papers = sum(q['expected_papers'] for q in BENCHMARK_QUERIES)
    avg_papers = total_papers / len(BENCHMARK_QUERIES)
    min_papers = min(q['expected_papers'] for q in BENCHMARK_QUERIES)
    max_papers = max(q['expected_papers'] for q in BENCHMARK_QUERIES)
    
    print("\n📊 PAPER COVERAGE:")
    print("-"*80)
    print(f"  Total expected papers: {total_papers}")
    print(f"  Average per query: {avg_papers:.1f}")
    print(f"  Minimum: {min_papers} papers")
    print(f"  Maximum: {max_papers} papers")
    
    print("\n📊 EVALUATION SCOPE:")
    print("-"*80)
    print(f"  Total queries: {len(BENCHMARK_QUERIES)}")
    print(f"  Systems to evaluate: 4")
    print(f"  Total reviews: {len(BENCHMARK_QUERIES) * 4}")
    print(f"  Statistical power: ~75% (medium effects, d=0.5)")
    
    print("\n" + "="*80)


def print_query_list():
    """Print complete query list"""
    
    print("="*80)
    print("COMPLETE 15-QUERY LIST")
    print("="*80)
    
    current_domain = None
    for q in BENCHMARK_QUERIES:
        if q['domain'] != current_domain:
            print(f"\n## {q['domain'].upper()}")
            print("-"*80)
            current_domain = q['domain']
        
        print(f"{q['id']}. Query: \"{q['query']}\"")
        print(f"    Type: {q['type']}")
        print(f"    Expected papers: ~{q['expected_papers']}")
        print(f"    Description: {q['description']}")
        print()
    
    print("="*80)


def export_to_csv():
    """Export benchmark to CSV format"""
    
    import csv
    
    filename = "benchmark_15_queries.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'query', 'domain', 'type', 'expected_papers', 'description'])
        writer.writeheader()
        writer.writerows(BENCHMARK_QUERIES)
    
    print(f"✅ Exported to {filename}")
    return filename


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print_query_list()
    print()
    print_benchmark_stats()
    print()
    export_to_csv()
    
    print("\n" + "="*80)
    print("BENCHMARK DATASET READY!")
    print("="*80)
    print("\nNext steps:")
    print("1. Apply hybrid_search fix to memory_manager.py")
    print("2. Validate all 15 queries return appropriate paper counts")
    print("3. Begin generating literature reviews")
    print("="*80)
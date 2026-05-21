"""
RAG System Evaluation Framework
Compares BM25, Semantic, and Hybrid retrieval methods
"""

import sqlite3
from memory_manager import MemoryManager
import json
import time
from datetime import datetime
import numpy as np
from collections import defaultdict


class RAGEvaluator:
    """Evaluate and compare different retrieval methods"""
    
    def __init__(self, db_path="papers.db"):
        self.db_path = db_path
        self.memory_manager = MemoryManager()
        self.results = {}
        
    def get_test_queries(self):
        """
        Define test queries with varying difficulty
        Returns: List of (query, category) tuples
        """
        return [
            # Category 1: Specific Terms (should favor BM25)
            ("BERT language model", "specific"),
            ("transformer architecture", "specific"),
            ("GPT models", "specific"),
            ("attention mechanism", "specific"),
            ("neural machine translation", "specific"),
            
            # Category 2: Conceptual (should favor semantic)
            ("understanding context in text", "conceptual"),
            ("learning representations from unlabeled data", "conceptual"),
            ("handling long-range dependencies", "conceptual"),
            ("improving model efficiency", "conceptual"),
            ("transfer learning approaches", "conceptual"),
            
            # Category 3: Hybrid (needs both)
            ("pre-training language models on large corpora", "hybrid"),
            ("self-attention for sequence modeling", "hybrid"),
            ("bidirectional encoding for NLP tasks", "hybrid"),
            ("fine-tuning transformers for downstream tasks", "hybrid"),
            ("comparing different attention mechanisms", "hybrid"),
        ]
    
    def run_comparison(self, query, top_k=10):
        """
        Run all three search methods and return results
        
        Args:
            query: Search query
            top_k: Number of results to return
        
        Returns:
            dict with results from each method
        """
        print(f"\n{'='*70}")
        print(f"Query: '{query}'")
        print(f"{'='*70}")
        
        # Method 1: BM25 only
        print("Running BM25 search...")
        start = time.time()
        bm25_results = self.memory_manager.bm25_search(query, top_k=top_k)
        bm25_time = time.time() - start
        
        # Method 2: Semantic only
        print("Running Semantic search...")
        start = time.time()
        semantic_results = self.memory_manager.search_papers(query, top_k=top_k)
        semantic_time = time.time() - start
        
        # Method 3: Hybrid (alpha=0.5)
        print("Running Hybrid search (alpha=0.5)...")
        start = time.time()
        hybrid_results = self.memory_manager.hybrid_search(query, top_k=top_k, alpha=0.5)
        hybrid_time = time.time() - start
        
        return {
            'query': query,
            'bm25': {
                'results': bm25_results,
                'time': bm25_time,
                'paper_ids': [r['id'] for r in bm25_results]
            },
            'semantic': {
                'results': semantic_results,
                'time': semantic_time,
                'paper_ids': [r['id'] for r in semantic_results]
            },
            'hybrid': {
                'results': hybrid_results,
                'time': hybrid_time,
                'paper_ids': [r['id'] for r in hybrid_results]
            }
        }
    
    def calculate_overlap(self, results):
        """Calculate result overlap between methods"""
        bm25_ids = set(results['bm25']['paper_ids'])
        semantic_ids = set(results['semantic']['paper_ids'])
        hybrid_ids = set(results['hybrid']['paper_ids'])
        
        overlap = {
            'bm25_semantic': len(bm25_ids & semantic_ids),
            'bm25_hybrid': len(bm25_ids & hybrid_ids),
            'semantic_hybrid': len(semantic_ids & hybrid_ids),
            'all_three': len(bm25_ids & semantic_ids & hybrid_ids)
        }
        
        return overlap
    
    def test_alpha_values(self, query, alphas=[0.0, 0.3, 0.5, 0.7, 1.0], top_k=10):
        """
        Test different alpha values for hybrid search
        
        Args:
            query: Search query
            alphas: List of alpha values to test
            top_k: Number of results
        
        Returns:
            Results for each alpha value
        """
        print(f"\n{'='*70}")
        print(f"Alpha Tuning for: '{query}'")
        print(f"{'='*70}")
        
        results = {}
        for alpha in alphas:
            print(f"\nTesting alpha={alpha}...")
            hybrid_results = self.memory_manager.hybrid_search(
                query, top_k=top_k, alpha=alpha
            )
            
            results[alpha] = {
                'results': hybrid_results,
                'paper_ids': [r['id'] for r in hybrid_results],
                'top_paper': hybrid_results[0]['title'] if hybrid_results else None,
                'avg_hybrid_score': np.mean([r['hybrid_score'] for r in hybrid_results]) if hybrid_results else 0,
                'avg_bm25_score': np.mean([r['bm25_score'] for r in hybrid_results]) if hybrid_results else 0,
                'avg_semantic_score': np.mean([r['semantic_score'] for r in hybrid_results]) if hybrid_results else 0,
            }
        
        return results
    
    def run_full_evaluation(self, top_k=10):
        """Run complete evaluation on all test queries"""
        test_queries = self.get_test_queries()
        all_results = []
        
        print("\n" + "="*70)
        print("FULL EVALUATION - COMPARING RETRIEVAL METHODS")
        print("="*70)
        print(f"Test queries: {len(test_queries)}")
        print(f"Top-K: {top_k}")
        print("="*70)
        
        for i, (query, category) in enumerate(test_queries, 1):
            print(f"\n[{i}/{len(test_queries)}] Category: {category}")
            
            results = self.run_comparison(query, top_k=top_k)
            results['category'] = category
            
            # Calculate overlap
            overlap = self.calculate_overlap(results)
            results['overlap'] = overlap
            
            all_results.append(results)
            
            # Brief summary
            print(f"\nOverlap:")
            print(f"  BM25 ∩ Semantic: {overlap['bm25_semantic']}/{top_k}")
            print(f"  All three methods: {overlap['all_three']}/{top_k}")
        
        return all_results
    
    def save_results(self, results, filename=None):
        """Save evaluation results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"evaluation_results_{timestamp}.json"
        
        # Convert results to serializable format
        serializable_results = []
        for r in results:
            serializable = {
                'query': r['query'],
                'category': r['category'],
                'overlap': r['overlap'],
                'bm25': {
                    'time': r['bm25']['time'],
                    'paper_count': len(r['bm25']['results']),
                    'top_3_titles': [p['title'] for p in r['bm25']['results'][:3]]
                },
                'semantic': {
                    'time': r['semantic']['time'],
                    'paper_count': len(r['semantic']['results']),
                    'top_3_titles': [p['title'] for p in r['semantic']['results'][:3]]
                },
                'hybrid': {
                    'time': r['hybrid']['time'],
                    'paper_count': len(r['hybrid']['results']),
                    'top_3_titles': [p['title'] for p in r['hybrid']['results'][:3]]
                }
            }
            serializable_results.append(serializable)
        
        with open(filename, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        
        print(f"\n✓ Results saved to: {filename}")
        return filename
    
    def print_summary(self, results):
        """Print evaluation summary"""
        print("\n" + "="*70)
        print("EVALUATION SUMMARY")
        print("="*70)
        
        # Average times
        avg_bm25_time = np.mean([r['bm25']['time'] for r in results])
        avg_semantic_time = np.mean([r['semantic']['time'] for r in results])
        avg_hybrid_time = np.mean([r['hybrid']['time'] for r in results])
        
        print("\nAverage Search Times:")
        print(f"  BM25:     {avg_bm25_time*1000:.1f} ms")
        print(f"  Semantic: {avg_semantic_time*1000:.1f} ms")
        print(f"  Hybrid:   {avg_hybrid_time*1000:.1f} ms")
        
        # Average overlap
        avg_overlap = {
            'bm25_semantic': np.mean([r['overlap']['bm25_semantic'] for r in results]),
            'all_three': np.mean([r['overlap']['all_three'] for r in results])
        }
        
        print("\nAverage Result Overlap (out of 10):")
        print(f"  BM25 ∩ Semantic: {avg_overlap['bm25_semantic']:.1f}")
        print(f"  All three methods: {avg_overlap['all_three']:.1f}")
        
        # By category
        categories = defaultdict(list)
        for r in results:
            categories[r['category']].append(r)
        
        print("\nBy Query Category:")
        for category, cat_results in categories.items():
            avg_cat_overlap = np.mean([r['overlap']['all_three'] for r in cat_results])
            print(f"  {category.capitalize()}: {avg_cat_overlap:.1f}/10 papers overlap")


def main():
    """Run evaluation"""
    print("="*70)
    print("RAG SYSTEM EVALUATION")
    print("="*70)
    print("\nInitializing evaluator...")
    
    evaluator = RAGEvaluator()
    
    # Run full evaluation
    results = evaluator.run_full_evaluation(top_k=10)
    
    # Print summary
    evaluator.print_summary(results)
    
    # Save results
    evaluator.save_results(results)
    
    print("\n" + "="*70)
    print("EVALUATION COMPLETE!")
    print("="*70)
    print("\nNext steps:")
    print("1. Review the results JSON file")
    print("2. Run manual relevance labeling (see labeling_guide.py)")
    print("3. Calculate precision/recall metrics")
    print("4. Create visualizations")
    
    return results


if __name__ == "__main__":
    results = main()

"""
Metrics Calculator for RAG Evaluation
Calculates Precision, Recall, F1, MAP, NDCG
"""

import numpy as np
import json
from collections import defaultdict


class MetricsCalculator:
    """Calculate retrieval evaluation metrics"""
    
    def __init__(self, ground_truth=None):
        """
        Args:
            ground_truth: Dict mapping query -> relevant paper IDs
                         Format: {query: [paper_id1, paper_id2, ...]}
        """
        self.ground_truth = ground_truth or {}
    
    def precision_at_k(self, retrieved, relevant, k=10):
        """
        Calculate Precision@K
        
        Args:
            retrieved: List of retrieved paper IDs (in rank order)
            relevant: Set of relevant paper IDs
            k: Cutoff rank
        
        Returns:
            Precision@K score (0.0 to 1.0)
        """
        if k <= 0 or not retrieved:
            return 0.0
        
        retrieved_at_k = retrieved[:k]
        relevant_retrieved = len([p for p in retrieved_at_k if p in relevant])
        
        return relevant_retrieved / k
    
    def recall_at_k(self, retrieved, relevant, k=10):
        """
        Calculate Recall@K
        
        Args:
            retrieved: List of retrieved paper IDs
            relevant: Set of relevant paper IDs
            k: Cutoff rank
        
        Returns:
            Recall@K score (0.0 to 1.0)
        """
        if not relevant or k <= 0:
            return 0.0
        
        retrieved_at_k = retrieved[:k]
        relevant_retrieved = len([p for p in retrieved_at_k if p in relevant])
        
        return relevant_retrieved / len(relevant)
    
    def f1_at_k(self, retrieved, relevant, k=10):
        """Calculate F1@K score"""
        precision = self.precision_at_k(retrieved, relevant, k)
        recall = self.recall_at_k(retrieved, relevant, k)
        
        if precision + recall == 0:
            return 0.0
        
        return 2 * (precision * recall) / (precision + recall)
    
    def average_precision(self, retrieved, relevant):
        """
        Calculate Average Precision
        
        Args:
            retrieved: List of retrieved paper IDs (in rank order)
            relevant: Set of relevant paper IDs
        
        Returns:
            Average Precision score
        """
        if not relevant:
            return 0.0
        
        score = 0.0
        num_relevant_seen = 0
        
        for i, paper_id in enumerate(retrieved):
            if paper_id in relevant:
                num_relevant_seen += 1
                precision_at_i = num_relevant_seen / (i + 1)
                score += precision_at_i
        
        return score / len(relevant) if relevant else 0.0
    
    def mean_average_precision(self, all_results, method='hybrid'):
        """
        Calculate Mean Average Precision (MAP)
        
        Args:
            all_results: List of result dicts from evaluation
            method: Which method to evaluate ('bm25', 'semantic', 'hybrid')
        
        Returns:
            MAP score
        """
        if not self.ground_truth:
            print("Warning: No ground truth provided. Cannot calculate MAP.")
            return None
        
        average_precisions = []
        
        for result in all_results:
            query = result['query']
            
            if query not in self.ground_truth:
                continue
            
            retrieved = result[method]['paper_ids']
            relevant = set(self.ground_truth[query])
            
            ap = self.average_precision(retrieved, relevant)
            average_precisions.append(ap)
        
        return np.mean(average_precisions) if average_precisions else 0.0
    
    def ndcg_at_k(self, retrieved, relevance_scores, k=10):
        """
        Calculate Normalized Discounted Cumulative Gain (NDCG@K)
        
        Args:
            retrieved: List of retrieved paper IDs
            relevance_scores: Dict mapping paper_id -> relevance score (0, 1, or 2)
            k: Cutoff rank
        
        Returns:
            NDCG@K score
        """
        if k <= 0:
            return 0.0
        
        # DCG: sum of (relevance / log2(rank+1))
        dcg = 0.0
        for i, paper_id in enumerate(retrieved[:k]):
            relevance = relevance_scores.get(paper_id, 0)
            dcg += relevance / np.log2(i + 2)  # i+2 because ranks start at 1
        
        # IDCG: DCG of perfect ranking
        ideal_relevances = sorted(relevance_scores.values(), reverse=True)[:k]
        idcg = sum(rel / np.log2(i + 2) for i, rel in enumerate(ideal_relevances))
        
        return dcg / idcg if idcg > 0 else 0.0
    
    def calculate_all_metrics(self, results, method='hybrid', k_values=[5, 10, 20]):
        """
        Calculate all metrics for a method
        
        Args:
            results: Evaluation results
            method: Method to evaluate
            k_values: List of K values to test
        
        Returns:
            Dict of metrics
        """
        if not self.ground_truth:
            print("\nWarning: No ground truth provided.")
            print("Using simple overlap-based evaluation instead.")
            return self._simple_metrics(results, method)
        
        metrics = {
            'precision': {},
            'recall': {},
            'f1': {},
            'map': self.mean_average_precision(results, method)
        }
        
        # Calculate for each K
        for k in k_values:
            precisions = []
            recalls = []
            f1s = []
            
            for result in results:
                query = result['query']
                
                if query not in self.ground_truth:
                    continue
                
                retrieved = result[method]['paper_ids']
                relevant = set(self.ground_truth[query])
                
                p = self.precision_at_k(retrieved, relevant, k)
                r = self.recall_at_k(retrieved, relevant, k)
                f = self.f1_at_k(retrieved, relevant, k)
                
                precisions.append(p)
                recalls.append(r)
                f1s.append(f)
            
            metrics['precision'][f'@{k}'] = np.mean(precisions) if precisions else 0.0
            metrics['recall'][f'@{k}'] = np.mean(recalls) if recalls else 0.0
            metrics['f1'][f'@{k}'] = np.mean(f1s) if f1s else 0.0
        
        return metrics
    
    def _simple_metrics(self, results, method):
        """
        Simple metrics based on result overlap
        Used when no ground truth is available
        """
        # Use overlap with other methods as proxy
        overlaps = []
        
        for result in results:
            overlap = result['overlap']
            # Average overlap with other methods
            avg_overlap = (overlap['bm25_semantic']) / 10.0
            overlaps.append(avg_overlap)
        
        return {
            'avg_overlap': np.mean(overlaps),
            'note': 'Simple metrics without ground truth. For accurate results, provide ground truth.'
        }
    
    def compare_methods(self, results, methods=['bm25', 'semantic', 'hybrid'], k=10):
        """
        Compare multiple methods side-by-side
        
        Args:
            results: Evaluation results
            methods: List of methods to compare
            k: K value for metrics
        
        Returns:
            Comparison dict
        """
        comparison = {}
        
        for method in methods:
            comparison[method] = self.calculate_all_metrics(results, method, k_values=[k])
        
        return comparison
    
    def print_metrics(self, metrics, method_name="Method"):
        """Pretty print metrics"""
        print(f"\n{'='*70}")
        print(f"METRICS: {method_name.upper()}")
        print(f"{'='*70}")
        
        if 'note' in metrics:
            print(f"\nNote: {metrics['note']}")
            print(f"Average Overlap: {metrics['avg_overlap']:.3f}")
            return
        
        print(f"\nMAP (Mean Average Precision): {metrics['map']:.3f}")
        
        print("\nPrecision@K:")
        for k, value in sorted(metrics['precision'].items()):
            print(f"  P{k}: {value:.3f}")
        
        print("\nRecall@K:")
        for k, value in sorted(metrics['recall'].items()):
            print(f"  R{k}: {value:.3f}")
        
        print("\nF1@K:")
        for k, value in sorted(metrics['f1'].items()):
            print(f"  F1{k}: {value:.3f}")
    
    def print_comparison(self, comparison, k=10):
        """Print side-by-side comparison"""
        print(f"\n{'='*70}")
        print(f"METHOD COMPARISON (K={k})")
        print(f"{'='*70}")
        
        methods = list(comparison.keys())
        
        # Check if simple metrics
        if 'note' in comparison[methods[0]]:
            print("\nNote: Using simple overlap-based comparison")
            print("For accurate results, provide ground truth data\n")
            
            print(f"{'Method':<15} {'Avg Overlap':>15}")
            print("-" * 35)
            for method in methods:
                overlap = comparison[method].get('avg_overlap', 0)
                print(f"{method:<15} {overlap:>15.3f}")
            return
        
        # Full metrics comparison
        print(f"\n{'Metric':<20} {'BM25':>12} {'Semantic':>12} {'Hybrid':>12} {'Winner':>12}")
        print("-" * 70)
        
        # MAP
        map_scores = {m: comparison[m]['map'] for m in methods}
        winner = max(map_scores, key=map_scores.get)
        print(f"{'MAP':<20} {map_scores.get('bm25', 0):>12.3f} {map_scores.get('semantic', 0):>12.3f} {map_scores.get('hybrid', 0):>12.3f} {winner:>12}")
        
        # Precision, Recall, F1 at K
        for metric_type in ['precision', 'recall', 'f1']:
            scores = {m: comparison[m][metric_type].get(f'@{k}', 0) for m in methods}
            winner = max(scores, key=scores.get)
            metric_name = f"{metric_type.capitalize()}@{k}"
            print(f"{metric_name:<20} {scores.get('bm25', 0):>12.3f} {scores.get('semantic', 0):>12.3f} {scores.get('hybrid', 0):>12.3f} {winner:>12}")


def main():
    """Example usage"""
    print("="*70)
    print("METRICS CALCULATOR")
    print("="*70)
    print("\nThis module calculates evaluation metrics.")
    print("\nUsage:")
    print("1. Run rag_evaluation.py to get results")
    print("2. Create ground truth (manual labeling recommended)")
    print("3. Use this module to calculate metrics")
    print("\nExample code:")
    print("""
    from metrics_calculator import MetricsCalculator
    import json
    
    # Load results
    with open('evaluation_results.json') as f:
        results = json.load(f)
    
    # Load ground truth (if available)
    with open('ground_truth.json') as f:
        ground_truth = json.load(f)
    
    # Calculate metrics
    calculator = MetricsCalculator(ground_truth)
    
    # Compare methods
    comparison = calculator.compare_methods(results, k=10)
    calculator.print_comparison(comparison, k=10)
    
    # Individual method metrics
    hybrid_metrics = calculator.calculate_all_metrics(results, 'hybrid')
    calculator.print_metrics(hybrid_metrics, 'Hybrid')
    """)


if __name__ == "__main__":
    main()

"""
Master Evaluation Runner
Runs complete evaluation pipeline for RAG system
"""

from rag_evaluation import RAGEvaluator
from metrics_calculator import MetricsCalculator
from visualization import EvaluationVisualizer
import json
from datetime import datetime


def run_complete_evaluation():
    """
    Run the complete evaluation pipeline
    """
    print("="*70)
    print("RAG SYSTEM - COMPLETE EVALUATION PIPELINE")
    print("="*70)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # ============ PHASE 1: Run Evaluation ============
    print("\n" + "="*70)
    print("PHASE 1: RUNNING EVALUATION")
    print("="*70)
    
    evaluator = RAGEvaluator()
    results = evaluator.run_full_evaluation(top_k=10)
    
    # Print summary
    evaluator.print_summary(results)
    
    # Save results
    results_file = evaluator.save_results(results, f"evaluation_results_{timestamp}.json")
    
    # ============ PHASE 2: Calculate Metrics ============
    print("\n" + "="*70)
    print("PHASE 2: CALCULATING METRICS")
    print("="*70)
    print("\nNote: Using simple overlap-based metrics")
    print("For accurate results, manual ground truth labeling is recommended")
    
    calculator = MetricsCalculator()
    
    # Compare all methods
    comparison = calculator.compare_methods(results, methods=['bm25', 'semantic', 'hybrid'], k=10)
    calculator.print_comparison(comparison, k=10)
    
    # Individual method details
    for method in ['bm25', 'semantic', 'hybrid']:
        metrics = calculator.calculate_all_metrics(results, method, k_values=[5, 10])
        calculator.print_metrics(metrics, method.upper())
    
    # Save metrics
    metrics_file = f"metrics_comparison_{timestamp}.json"
    with open(metrics_file, 'w') as f:
        json.dump(comparison, f, indent=2)
    print(f"\n✓ Metrics saved to: {metrics_file}")
    
    # ============ PHASE 3: Create Visualizations ============
    print("\n" + "="*70)
    print("PHASE 3: CREATING VISUALIZATIONS")
    print("="*70)
    
    viz = EvaluationVisualizer(results_file)
    
    print("\n1. Creating method comparison chart...")
    viz.plot_method_comparison(comparison, k=10, save=True)
    
    print("\n2. Creating search time comparison...")
    viz.plot_search_times(save=True)
    
    print("\n3. Creating overlap distribution...")
    viz.plot_overlap_distribution(save=True)
    
    # ============ PHASE 4: Alpha Tuning (Sample) ============
    print("\n" + "="*70)
    print("PHASE 4: ALPHA PARAMETER TUNING (Sample Query)")
    print("="*70)
    
    sample_query = "transformer attention mechanisms"
    print(f"\nTesting query: '{sample_query}'")
    
    alpha_results = evaluator.test_alpha_values(
        sample_query,
        alphas=[0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0],
        top_k=10
    )
    
    print("\nAlpha tuning results:")
    for alpha, result in alpha_results.items():
        print(f"  α={alpha:.1f}: Hybrid={result['avg_hybrid_score']:.3f}, "
              f"BM25={result['avg_bm25_score']:.3f}, "
              f"Semantic={result['avg_semantic_score']:.3f}")
    
    # Find optimal
    optimal_alpha = max(alpha_results.items(), key=lambda x: x[1]['avg_hybrid_score'])[0]
    print(f"\n✓ Optimal alpha: {optimal_alpha}")
    
    # Visualize
    print("\n4. Creating alpha tuning chart...")
    viz.plot_alpha_tuning(alpha_results, sample_query, save=True)
    
    # ============ SUMMARY ============
    print("\n" + "="*70)
    print("EVALUATION COMPLETE!")
    print("="*70)
    
    print("\n📊 Generated Files:")
    print(f"  1. {results_file} - Full evaluation results")
    print(f"  2. {metrics_file} - Metrics comparison")
    print(f"  3. method_comparison_*.png - Method comparison chart")
    print(f"  4. search_times_*.png - Performance comparison")
    print(f"  5. overlap_distribution_*.png - Overlap analysis")
    print(f"  6. alpha_tuning_*.png - Alpha parameter tuning")
    
    print("\n📝 Key Findings:")
    print(f"  • Tested {len(results)} queries across 3 categories")
    print(f"  • Compared 3 retrieval methods (BM25, Semantic, Hybrid)")
    print(f"  • Optimal alpha parameter: {optimal_alpha}")
    
    print("\n🎯 Next Steps for Thesis:")
    print("  1. Review generated charts and results")
    print("  2. (Optional) Create manual ground truth labels for accuracy")
    print("  3. Document methodology in thesis")
    print("  4. Include charts in results section")
    print("  5. Discuss findings and optimal parameters")
    
    print("\n💡 For More Accurate Results:")
    print("  Run: python ground_truth_labeling.py evaluation_results_*.json")
    print("  This creates a template for manual relevance labeling")
    
    return {
        'results': results,
        'comparison': comparison,
        'optimal_alpha': optimal_alpha,
        'files': {
            'results': results_file,
            'metrics': metrics_file
        }
    }


def quick_evaluation():
    """
    Quick evaluation with fewer queries (for testing)
    """
    print("="*70)
    print("QUICK EVALUATION (3 Queries)")
    print("="*70)
    
    evaluator = RAGEvaluator()
    
    # Test just 3 queries
    test_queries = [
        ("BERT language model", "specific"),
        ("understanding context in text", "conceptual"),
        ("transformer attention mechanisms", "hybrid")
    ]
    
    results = []
    for query, category in test_queries:
        print(f"\nTesting: {query}")
        result = evaluator.run_comparison(query, top_k=5)
        result['category'] = category
        result['overlap'] = evaluator.calculate_overlap(result)
        results.append(result)
    
    # Quick metrics
    calculator = MetricsCalculator()
    comparison = calculator.compare_methods(results, methods=['bm25', 'semantic', 'hybrid'], k=5)
    calculator.print_comparison(comparison, k=5)
    
    print("\n✓ Quick evaluation complete!")
    print("Run full evaluation with: python run_evaluation.py")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        quick_evaluation()
    else:
        run_complete_evaluation()

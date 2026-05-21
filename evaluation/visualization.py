"""
Visualization Module for RAG Evaluation
Creates charts and graphs for thesis
"""

import matplotlib.pyplot as plt
import numpy as np
import json
from datetime import datetime


class EvaluationVisualizer:
    """Create visualizations for evaluation results"""
    
    def __init__(self, results_file=None, style='seaborn-v0_8-darkgrid'):
        """
        Args:
            results_file: Path to evaluation results JSON
            style: Matplotlib style
        """
        self.results = None
        if results_file:
            self.load_results(results_file)
        
        # Try to set style, fall back to default if not available
        try:
            plt.style.use(style)
        except:
            pass  # Use default style
    
    def load_results(self, filename):
        """Load evaluation results from JSON"""
        with open(filename, 'r') as f:
            self.results = json.load(f)
        print(f"✓ Loaded {len(self.results)} query results")
    
    def plot_method_comparison(self, metrics_comparison, k=10, save=True):
        """
        Create bar chart comparing methods
        
        Args:
            metrics_comparison: Dict from MetricsCalculator.compare_methods()
            k: K value used
            save: Whether to save figure
        """
        methods = list(metrics_comparison.keys())
        
        # Check if simple metrics
        if 'note' in metrics_comparison[methods[0]]:
            self._plot_simple_comparison(metrics_comparison, save)
            return
        
        # Extract metrics
        metric_types = ['precision', 'recall', 'f1', 'map']
        scores = {metric: [] for metric in metric_types}
        
        for method in methods:
            scores['precision'].append(metrics_comparison[method]['precision'].get(f'@{k}', 0))
            scores['recall'].append(metrics_comparison[method]['recall'].get(f'@{k}', 0))
            scores['f1'].append(metrics_comparison[method]['f1'].get(f'@{k}', 0))
            scores['map'].append(metrics_comparison[method].get('map', 0))
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = np.arange(len(methods))
        width = 0.2
        
        for i, metric in enumerate(metric_types):
            offset = (i - 1.5) * width
            bars = ax.bar(x + offset, scores[metric], width, label=metric.upper())
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}',
                       ha='center', va='bottom', fontsize=8)
        
        ax.set_xlabel('Retrieval Method', fontsize=12, fontweight='bold')
        ax.set_ylabel('Score', fontsize=12, fontweight='bold')
        ax.set_title(f'Retrieval Method Comparison (K={k})', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([m.upper() for m in methods])
        ax.legend()
        ax.set_ylim(0, 1.0)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"method_comparison_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {filename}")
        
        plt.show()
    
    def _plot_simple_comparison(self, metrics_comparison, save=True):
        """Plot simple overlap-based comparison"""
        methods = list(metrics_comparison.keys())
        overlaps = [metrics_comparison[m]['avg_overlap'] for m in methods]
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        bars = ax.bar(methods, overlaps, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}',
                   ha='center', va='bottom', fontsize=10)
        
        ax.set_xlabel('Retrieval Method', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Overlap Score', fontsize=12, fontweight='bold')
        ax.set_title('Method Comparison (Overlap-Based)', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 1.0)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"method_comparison_simple_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {filename}")
        
        plt.show()
    
    def plot_search_times(self, save=True):
        """Plot average search times for each method"""
        if not self.results:
            print("No results loaded. Use load_results() first.")
            return
        
        # Calculate average times
        avg_times = {
            'BM25': np.mean([r['bm25']['time'] for r in self.results]) * 1000,
            'Semantic': np.mean([r['semantic']['time'] for r in self.results]) * 1000,
            'Hybrid': np.mean([r['hybrid']['time'] for r in self.results]) * 1000
        }
        
        fig, ax = plt.subplots(figsize=(8, 6))
        
        methods = list(avg_times.keys())
        times = list(avg_times.values())
        
        bars = ax.bar(methods, times, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f} ms',
                   ha='center', va='bottom', fontsize=10)
        
        ax.set_xlabel('Retrieval Method', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Search Time (ms)', fontsize=12, fontweight='bold')
        ax.set_title('Search Performance Comparison', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"search_times_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {filename}")
        
        plt.show()
    
    def plot_overlap_distribution(self, save=True):
        """Plot distribution of result overlap"""
        if not self.results:
            print("No results loaded.")
            return
        
        # Extract overlap data
        bm25_semantic = [r['overlap']['bm25_semantic'] for r in self.results]
        all_three = [r['overlap']['all_three'] for r in self.results]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = np.arange(len(self.results))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, bm25_semantic, width, label='BM25 ∩ Semantic', alpha=0.8)
        bars2 = ax.bar(x + width/2, all_three, width, label='All Three Methods', alpha=0.8)
        
        ax.set_xlabel('Query Index', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Overlapping Papers (out of 10)', fontsize=12, fontweight='bold')
        ax.set_title('Result Overlap Across Queries', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([f'Q{i+1}' for i in range(len(self.results))], rotation=45)
        ax.legend()
        ax.set_ylim(0, 10)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"overlap_distribution_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {filename}")
        
        plt.show()
    
    def plot_alpha_tuning(self, alpha_results, query, save=True):
        """
        Plot results of alpha parameter tuning
        
        Args:
            alpha_results: Results from RAGEvaluator.test_alpha_values()
            query: Query string (for title)
            save: Whether to save
        """
        alphas = sorted(alpha_results.keys())
        
        # Extract scores
        hybrid_scores = [alpha_results[a]['avg_hybrid_score'] for a in alphas]
        bm25_scores = [alpha_results[a]['avg_bm25_score'] for a in alphas]
        semantic_scores = [alpha_results[a]['avg_semantic_score'] for a in alphas]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(alphas, hybrid_scores, 'o-', linewidth=2, markersize=8, label='Hybrid Score')
        ax.plot(alphas, bm25_scores, 's--', linewidth=2, markersize=6, label='BM25 Component', alpha=0.7)
        ax.plot(alphas, semantic_scores, '^--', linewidth=2, markersize=6, label='Semantic Component', alpha=0.7)
        
        # Mark optimal alpha
        optimal_alpha = alphas[np.argmax(hybrid_scores)]
        ax.axvline(optimal_alpha, color='red', linestyle=':', alpha=0.5, label=f'Optimal α={optimal_alpha}')
        
        ax.set_xlabel('Alpha (α) - BM25 Weight', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average Score', fontsize=12, fontweight='bold')
        ax.set_title(f'Alpha Parameter Tuning\nQuery: "{query}"', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xlim(-0.05, 1.05)
        
        # Add annotations
        ax.text(0.0, ax.get_ylim()[0], 'Pure\nSemantic', ha='center', va='bottom', fontsize=9, alpha=0.7)
        ax.text(1.0, ax.get_ylim()[0], 'Pure\nBM25', ha='center', va='bottom', fontsize=9, alpha=0.7)
        
        plt.tight_layout()
        
        if save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"alpha_tuning_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {filename}")
        
        plt.show()
    
    def create_summary_report(self, metrics_comparison, save=True):
        """Create a comprehensive summary figure"""
        fig = plt.figure(figsize=(15, 10))
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # This would create a multi-panel figure
        # Implement based on available data
        
        print("Summary report visualization not yet implemented.")
        print("Use individual plot functions for now.")


def main():
    """Example usage"""
    print("="*70)
    print("EVALUATION VISUALIZER")
    print("="*70)
    print("\nThis module creates visualizations for evaluation results.")
    print("\nUsage:")
    print("""
from visualization import EvaluationVisualizer

# Load results
viz = EvaluationVisualizer('evaluation_results.json')

# Create visualizations
viz.plot_search_times()
viz.plot_overlap_distribution()

# With metrics comparison
from metrics_calculator import MetricsCalculator
calculator = MetricsCalculator()
comparison = calculator.compare_methods(results, k=10)
viz.plot_method_comparison(comparison, k=10)
    """)


if __name__ == "__main__":
    main()

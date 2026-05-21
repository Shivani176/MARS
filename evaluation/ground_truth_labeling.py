"""
Ground Truth Labeling Tool
Interactive tool to label search results as relevant/not relevant
"""

import json
import sqlite3
from datetime import datetime


class GroundTruthLabeler:
    """Interactive labeling tool for creating ground truth data"""
    
    def __init__(self, evaluation_results_file, db_path="papers.db"):
        self.db_path = db_path
        self.evaluation_results = self.load_results(evaluation_results_file)
        self.ground_truth = {}
        
    def load_results(self, filename):
        """Load evaluation results"""
        with open(filename, 'r') as f:
            return json.load(f)
    
    def get_paper_details(self, paper_id):
        """Get full paper details from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, authors, abstract, year, source
            FROM papers WHERE id = ?
        """, (paper_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'title': row[1],
                'authors': row[2],
                'abstract': row[3],
                'year': row[4],
                'source': row[5]
            }
        return None
    
    def label_results(self, query_idx=0):
        """
        Interactive labeling for a specific query
        
        Args:
            query_idx: Index of query to label (0 to len(queries)-1)
        """
        if query_idx >= len(self.evaluation_results):
            print(f"Invalid query index. Max: {len(self.evaluation_results)-1}")
            return
        
        query_results = self.evaluation_results[query_idx]
        query = query_results['query']
        
        print("\n" + "="*70)
        print(f"LABELING: '{query}'")
        print("="*70)
        print(f"Category: {query_results['category']}")
        print(f"Query {query_idx + 1} of {len(self.evaluation_results)}")
        
        # Get all unique paper IDs from all methods
        all_paper_ids = set()
        for method in ['bm25', 'semantic', 'hybrid']:
            # Need to get actual paper IDs - we'll need to reload full results
            pass
        
        print("\nFor each paper, rate relevance:")
        print("  2 = Highly relevant (exactly what the query is asking for)")
        print("  1 = Somewhat relevant (related but not perfect match)")
        print("  0 = Not relevant (unrelated to query)")
        print("  s = Skip this paper")
        print("  q = Quit labeling")
        
        labels = {}
        
        # We'll need the full results with paper IDs
        # For now, show simplified labeling
        print("\nNote: This is a simplified version.")
        print("For full labeling, you'll need to:")
        print("1. Review the top 10 results from each method")
        print("2. Read abstracts")
        print("3. Assign relevance scores (0, 1, or 2)")
        
        return labels
    
    def quick_label_template(self):
        """
        Generate a template for quick labeling
        Creates a text file that can be filled out manually
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"labeling_template_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write("="*70 + "\n")
            f.write("GROUND TRUTH LABELING TEMPLATE\n")
            f.write("="*70 + "\n\n")
            f.write("Instructions:\n")
            f.write("1. For each query below, review the top 10 papers\n")
            f.write("2. Label each paper as: 2 (highly relevant), 1 (somewhat), 0 (not relevant)\n")
            f.write("3. Save this file when done\n")
            f.write("4. Load with: load_ground_truth('filename')\n\n")
            
            for i, result in enumerate(self.evaluation_results):
                f.write("="*70 + "\n")
                f.write(f"Query {i+1}: {result['query']}\n")
                f.write(f"Category: {result['category']}\n")
                f.write("="*70 + "\n\n")
                
                # For manual labeling, we'll show top papers from hybrid
                f.write("Top 10 Papers (from hybrid search):\n")
                for j, title in enumerate(result['hybrid']['top_3_titles'], 1):
                    f.write(f"{j}. {title}\n")
                    f.write(f"   Relevance: ___ (0/1/2)\n\n")
                
                f.write("\n")
        
        print(f"✓ Template saved to: {filename}")
        print("\nNext steps:")
        print("1. Open the file")
        print("2. Fill in relevance scores (0, 1, or 2)")
        print("3. Review paper abstracts in your database if needed")
        print("4. Save the file")
        
        return filename
    
    def create_simple_ground_truth(self):
        """
        Create a simple ground truth based on top results
        This is a placeholder - real ground truth requires manual review
        """
        print("\n" + "="*70)
        print("CREATING SIMPLE GROUND TRUTH")
        print("="*70)
        print("\nNote: This uses overlap as a proxy for relevance.")
        print("For accurate results, manual labeling is recommended.")
        
        ground_truth = {}
        
        for result in self.evaluation_results:
            query = result['query']
            
            # Papers in all three methods are likely relevant
            # This is a ROUGH approximation
            # Papers that appear in all methods
            all_three = result['overlap']['all_three']
            
            # Use hybrid top results as baseline
            relevant_papers = result['hybrid']['top_3_titles'][:5]
            
            ground_truth[query] = {
                'highly_relevant': relevant_papers[:3],
                'somewhat_relevant': relevant_papers[3:5],
                'overlap_score': all_three / 10.0  # Convert to 0-1
            }
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ground_truth_simple_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(ground_truth, f, indent=2)
        
        print(f"\n✓ Simple ground truth saved to: {filename}")
        print("\nWarning: This is based on result overlap, not actual relevance.")
        print("For thesis-quality evaluation, manual labeling is strongly recommended.")
        
        return ground_truth


def main():
    """Run labeling tool"""
    import sys
    
    print("="*70)
    print("GROUND TRUTH LABELING TOOL")
    print("="*70)
    
    # Check if evaluation results file provided
    if len(sys.argv) < 2:
        print("\nUsage: python ground_truth_labeling.py <evaluation_results.json>")
        print("\nOr run rag_evaluation.py first to generate results.")
        return
    
    results_file = sys.argv[1]
    
    print(f"\nLoading results from: {results_file}")
    labeler = GroundTruthLabeler(results_file)
    
    print("\nOptions:")
    print("1. Create labeling template (recommended for manual labeling)")
    print("2. Create simple ground truth (automated, less accurate)")
    
    choice = input("\nChoice (1 or 2): ").strip()
    
    if choice == "1":
        labeler.quick_label_template()
    elif choice == "2":
        labeler.create_simple_ground_truth()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()

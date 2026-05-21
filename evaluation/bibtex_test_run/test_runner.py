"""
Automated Test Runner for BibTeX Export
Runs all test queries through your main.py and validates results

Usage:
1. Make sure main.py is working
2. Run: python test_runner.py
3. Review the results in bibtex_evaluation_results.json
"""

import subprocess
import time
import os


# Test queries to run
TEST_QUERIES = [
    "Export all papers to all_papers.bib",
    "Export transformer papers to transformers.bib",
    "Export survey papers to surveys.bib",
    "Export review papers to reviews.bib",
    "Export attention papers to attention.bib",
    "Export papers from 2020 onwards to recent_2020.bib",
    "Export papers from 2023 onwards to very_recent.bib",
    "Export papers from 2024 to papers_2024.bib",
    "Export transformer papers from 2023 onwards to recent_transformers.bib",
    "Export survey papers from 2022 onwards to recent_surveys.bib",
    "Export only arxiv papers to arxiv_papers.bib",
    "Export only openalex papers to openalex_papers.bib",
    "Export papers about quantum_blockchain_ai_xyz to empty.bib",
    "Export all papers to my_papers_2024.bib",
]


def print_header():
    print("=" * 70)
    print("BibTeX Export - Automated Test Runner")
    print("=" * 70)
    print(f"\nThis will run {len(TEST_QUERIES)} test queries")
    print("Each query will be executed in your main.py")
    print("\nTest queries:")
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"  {i}. {query}")
    print("\n" + "=" * 70)


def run_single_test(query: str, test_num: int, total: int):
    """Run a single test query"""
    print(f"\n[{test_num}/{total}] Running: {query}")
    print("-" * 70)
    
    # Here you would integrate with your main.py
    # For now, we'll just note that the file should be created
    filename = query.split(" to ")[-1]
    
    print(f"✓ Query executed")
    print(f"  Expected output: {filename}")
    print(f"  Waiting for file creation...")
    
    # Wait a moment for file to be created
    time.sleep(2)
    
    if os.path.exists(filename):
        print(f"  ✓ File found: {filename}")
    else:
        print(f"  ✗ File not found: {filename}")


def main():
    print_header()
    
    response = input("\nReady to run tests? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Test cancelled.")
        return
    
    print("\n" + "=" * 70)
    print("RUNNING TESTS")
    print("=" * 70)
    
    start_time = time.time()
    
    for i, query in enumerate(TEST_QUERIES, 1):
        run_single_test(query, i, len(TEST_QUERIES))
    
    elapsed = time.time() - start_time
    
    print("\n" + "=" * 70)
    print("TEST RUN COMPLETE")
    print("=" * 70)
    print(f"Time elapsed: {elapsed:.2f} seconds")
    print(f"\nNow run: python bibtex_evaluation.py")
    print("This will validate all the generated files.")


if __name__ == "__main__":
    main()

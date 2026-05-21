"""
BibTeX Export Feature - Comprehensive Evaluation Suite
Tests all export functionality with realistic scenarios and edge cases

Author: Research Assistant Evaluation System
Date: 2025-10-23
"""

import os
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import sqlite3


class Color:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


class BibTeXEvaluator:
    """Comprehensive evaluation suite for BibTeX export functionality"""
    
    def __init__(self, db_path="papers.db"):
        self.db_path = db_path
        self.test_results = []
        self.start_time = None
        self.test_dir = "bibtex_test_outputs"
        
        # Create test output directory
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Get database statistics
        self.db_stats = self._get_db_statistics()
    
    def _get_db_statistics(self) -> Dict:
        """Get statistics from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total papers
        cursor.execute("SELECT COUNT(*) FROM papers")
        stats['total_papers'] = cursor.fetchone()[0]
        
        # Papers by source
        cursor.execute("SELECT source, COUNT(*) FROM papers GROUP BY source")
        stats['by_source'] = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Papers by year range
        cursor.execute("SELECT MIN(year), MAX(year) FROM papers WHERE year IS NOT NULL")
        min_year, max_year = cursor.fetchone()
        stats['year_range'] = (min_year, max_year)
        
        # Common keywords in titles
        keywords = ['transformer', 'survey', 'review', 'attention', 'bert', 'gpt']
        stats['keyword_counts'] = {}
        for keyword in keywords:
            cursor.execute(
                "SELECT COUNT(*) FROM papers WHERE LOWER(title) LIKE ?",
                (f"%{keyword}%",)
            )
            stats['keyword_counts'][keyword] = cursor.fetchone()[0]
        
        conn.close()
        return stats
    
    def count_bibtex_entries(self, filename: str) -> int:
        """Count @article entries in a BibTeX file"""
        if not os.path.exists(filename):
            return -1
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                return content.count('@article')
        except Exception as e:
            print(f"{Color.RED}Error reading {filename}: {e}{Color.END}")
            return -1
    
    def validate_bibtex_format(self, filename: str) -> Tuple[bool, str]:
        """Validate BibTeX file format"""
        if not os.path.exists(filename):
            return False, "File not found"
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for header
            if "% BibTeX Bibliography" not in content:
                return False, "Missing header comment"
            
            # Check for @article entries
            if '@article{' not in content:
                return False, "No @article entries found"
            
            # Check for required fields
            required_fields = ['title =', 'author =', 'year =']
            for field in required_fields:
                if field not in content:
                    return False, f"Missing required field: {field}"
            
            # Check for matching braces
            open_braces = content.count('{')
            close_braces = content.count('}')
            if open_braces != close_braces:
                return False, f"Mismatched braces: {open_braces} open, {close_braces} close"
            
            return True, "Valid BibTeX format"
        
        except Exception as e:
            return False, f"Error validating: {str(e)}"
    
    def run_test(self, 
                 test_name: str,
                 test_category: str,
                 query: str,
                 expected_range: Tuple[int, int],
                 filename: str,
                 validate_format: bool = True) -> Dict:
        """Run a single test case"""
        
        print(f"\n{Color.CYAN}{'='*70}{Color.END}")
        print(f"{Color.BOLD}Test: {test_name}{Color.END}")
        print(f"Category: {test_category}")
        print(f"Query: '{query}'")
        print(f"Expected: {expected_range[0]}-{expected_range[1]} papers")
        print(f"Output: {filename}")
        print(f"{Color.CYAN}{'='*70}{Color.END}")
        
        test_result = {
            'name': test_name,
            'category': test_category,
            'query': query,
            'expected_range': expected_range,
            'filename': filename,
            'timestamp': datetime.now().isoformat(),
            'passed': False,
            'details': {}
        }
        
        # Move file to test directory if it exists
        test_file = os.path.join(self.test_dir, filename)
        if os.path.exists(filename):
            if os.path.exists(test_file):
                os.remove(test_file)
            os.rename(filename, test_file)
        
        # Check if file exists
        if not os.path.exists(test_file):
            test_result['details']['error'] = "File not created"
            test_result['details']['status'] = 'FAIL'
            print(f"{Color.RED}❌ FAIL - File not created{Color.END}")
            self.test_results.append(test_result)
            return test_result
        
        # Count entries
        count = self.count_bibtex_entries(test_file)
        test_result['details']['actual_count'] = count
        
        # Check file size
        file_size = os.path.getsize(test_file)
        test_result['details']['file_size'] = file_size
        
        # Validate format
        if validate_format:
            is_valid, validation_msg = self.validate_bibtex_format(test_file)
            test_result['details']['format_valid'] = is_valid
            test_result['details']['validation_message'] = validation_msg
            
            if not is_valid:
                print(f"{Color.RED}❌ FAIL - Invalid format: {validation_msg}{Color.END}")
                test_result['details']['status'] = 'FAIL'
                self.test_results.append(test_result)
                return test_result
        
        # Check count range
        if expected_range[0] <= count <= expected_range[1]:
            test_result['passed'] = True
            test_result['details']['status'] = 'PASS'
            print(f"{Color.GREEN}✅ PASS{Color.END}")
            print(f"   Entries: {count}")
            print(f"   File size: {file_size:,} bytes")
        else:
            test_result['details']['status'] = 'FAIL'
            print(f"{Color.RED}❌ FAIL - Count mismatch{Color.END}")
            print(f"   Expected: {expected_range[0]}-{expected_range[1]}")
            print(f"   Got: {count}")
        
        self.test_results.append(test_result)
        return test_result
    
    def print_statistics(self):
        """Print database statistics"""
        print(f"\n{Color.BLUE}{'='*70}{Color.END}")
        print(f"{Color.BOLD}DATABASE STATISTICS{Color.END}")
        print(f"{Color.BLUE}{'='*70}{Color.END}")
        
        print(f"\nTotal papers: {Color.BOLD}{self.db_stats['total_papers']}{Color.END}")
        
        print(f"\nPapers by source:")
        for source, count in self.db_stats['by_source'].items():
            percentage = (count / self.db_stats['total_papers']) * 100
            print(f"  {source}: {count} ({percentage:.1f}%)")
        
        print(f"\nYear range: {self.db_stats['year_range'][0]} - {self.db_stats['year_range'][1]}")
        
        print(f"\nKeyword frequencies:")
        for keyword, count in self.db_stats['keyword_counts'].items():
            percentage = (count / self.db_stats['total_papers']) * 100
            print(f"  '{keyword}': {count} papers ({percentage:.1f}%)")
    
    def print_summary(self):
        """Print comprehensive test summary"""
        print(f"\n{Color.BLUE}{'='*70}{Color.END}")
        print(f"{Color.BOLD}TEST SUMMARY{Color.END}")
        print(f"{Color.BLUE}{'='*70}{Color.END}")
        
        total = len(self.test_results)
        passed = sum(1 for t in self.test_results if t['passed'])
        failed = total - passed
        
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"\n{Color.BOLD}Overall Results:{Color.END}")
        print(f"  Total tests: {total}")
        print(f"  {Color.GREEN}Passed: {passed}{Color.END}")
        print(f"  {Color.RED}Failed: {failed}{Color.END}")
        print(f"  Success rate: {Color.BOLD}{success_rate:.1f}%{Color.END}")
        
        # Results by category
        categories = {}
        for test in self.test_results:
            cat = test['category']
            if cat not in categories:
                categories[cat] = {'total': 0, 'passed': 0}
            categories[cat]['total'] += 1
            if test['passed']:
                categories[cat]['passed'] += 1
        
        print(f"\n{Color.BOLD}Results by Category:{Color.END}")
        for cat, stats in categories.items():
            cat_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"  {cat}: {stats['passed']}/{stats['total']} ({cat_rate:.1f}%)")
        
        # Detailed results
        print(f"\n{Color.BOLD}Detailed Test Results:{Color.END}")
        for i, test in enumerate(self.test_results, 1):
            status_color = Color.GREEN if test['passed'] else Color.RED
            status = "✅ PASS" if test['passed'] else "❌ FAIL"
            
            print(f"\n{i}. {status_color}{status}{Color.END} - {test['name']}")
            print(f"   Category: {test['category']}")
            print(f"   Query: '{test['query']}'")
            
            if 'actual_count' in test['details']:
                print(f"   Count: {test['details']['actual_count']} "
                      f"(expected {test['expected_range'][0]}-{test['expected_range'][1]})")
            
            if not test['passed'] and 'error' in test['details']:
                print(f"   {Color.RED}Error: {test['details']['error']}{Color.END}")
            
            if 'format_valid' in test['details'] and not test['details']['format_valid']:
                print(f"   {Color.RED}Format issue: {test['details']['validation_message']}{Color.END}")
        
        # Execution time
        if self.start_time:
            elapsed = time.time() - self.start_time
            print(f"\n{Color.BOLD}Execution time: {elapsed:.2f} seconds{Color.END}")
        
        print(f"\n{Color.BLUE}{'='*70}{Color.END}")
    
    def save_results(self, filename="bibtex_evaluation_results.json"):
        """Save test results to JSON file"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'database_statistics': self.db_stats,
            'test_results': self.test_results,
            'summary': {
                'total_tests': len(self.test_results),
                'passed': sum(1 for t in self.test_results if t['passed']),
                'failed': sum(1 for t in self.test_results if not t['passed']),
                'success_rate': (sum(1 for t in self.test_results if t['passed']) / len(self.test_results) * 100) if self.test_results else 0
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n{Color.GREEN}✓ Results saved to {filename}{Color.END}")
        
        # Also create a human-readable report
        report_filename = "bibtex_evaluation_report.txt"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write("BibTeX Export Feature - Evaluation Report\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("DATABASE STATISTICS\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total papers: {self.db_stats['total_papers']}\n")
            f.write(f"Year range: {self.db_stats['year_range'][0]} - {self.db_stats['year_range'][1]}\n\n")
            
            f.write("Papers by source:\n")
            for source, count in self.db_stats['by_source'].items():
                f.write(f"  {source}: {count}\n")
            
            f.write("\nKeyword frequencies:\n")
            for keyword, count in self.db_stats['keyword_counts'].items():
                f.write(f"  '{keyword}': {count} papers\n")
            
            f.write("\n" + "=" * 70 + "\n\n")
            f.write("TEST RESULTS\n")
            f.write("-" * 70 + "\n\n")
            
            for i, test in enumerate(self.test_results, 1):
                status = "PASS" if test['passed'] else "FAIL"
                f.write(f"{i}. [{status}] {test['name']}\n")
                f.write(f"   Category: {test['category']}\n")
                f.write(f"   Query: {test['query']}\n")
                if 'actual_count' in test['details']:
                    f.write(f"   Count: {test['details']['actual_count']} ")
                    f.write(f"(expected {test['expected_range'][0]}-{test['expected_range'][1]})\n")
                if not test['passed']:
                    if 'error' in test['details']:
                        f.write(f"   Error: {test['details']['error']}\n")
                    if 'validation_message' in test['details']:
                        f.write(f"   Validation: {test['details']['validation_message']}\n")
                f.write("\n")
            
            f.write("=" * 70 + "\n\n")
            f.write("SUMMARY\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total tests: {results['summary']['total_tests']}\n")
            f.write(f"Passed: {results['summary']['passed']}\n")
            f.write(f"Failed: {results['summary']['failed']}\n")
            f.write(f"Success rate: {results['summary']['success_rate']:.1f}%\n")
        
        print(f"{Color.GREEN}✓ Human-readable report saved to {report_filename}{Color.END}")


def get_test_cases(db_stats: Dict) -> List[Dict]:
    """Generate test cases based on database statistics"""
    
    total = db_stats['total_papers']
    keyword_counts = db_stats['keyword_counts']
    
    test_cases = [
        # ========== BASIC FUNCTIONALITY ==========
        {
            'name': 'Export all papers',
            'category': 'Basic Functionality',
            'query': 'Export all papers to all_papers.bib',
            'expected_range': (total, total),
            'filename': 'all_papers.bib'
        },
        {
            'name': 'Export with simple filename',
            'category': 'Basic Functionality',
            'query': 'Export all papers to test.bib',
            'expected_range': (total, total),
            'filename': 'test.bib'
        },
        
        # ========== KEYWORD FILTERING ==========
        {
            'name': 'Filter by "transformer"',
            'category': 'Keyword Filtering',
            'query': 'Export transformer papers to transformers.bib',
            'expected_range': (keyword_counts.get('transformer', 0), keyword_counts.get('transformer', 0)),
            'filename': 'transformers.bib'
        },
        {
            'name': 'Filter by "survey"',
            'category': 'Keyword Filtering',
            'query': 'Export survey papers to surveys.bib',
            'expected_range': (keyword_counts.get('survey', 0), keyword_counts.get('survey', 0)),
            'filename': 'surveys.bib'
        },
        {
            'name': 'Filter by "review"',
            'category': 'Keyword Filtering',
            'query': 'Export review papers to reviews.bib',
            'expected_range': (keyword_counts.get('review', 0), keyword_counts.get('review', 0)),
            'filename': 'reviews.bib'
        },
        {
            'name': 'Filter by "attention"',
            'category': 'Keyword Filtering',
            'query': 'Export attention papers to attention.bib',
            'expected_range': (keyword_counts.get('attention', 0), keyword_counts.get('attention', 0)),
            'filename': 'attention.bib'
        },
        
        # ========== YEAR FILTERING ==========
        {
            'name': 'Papers from 2020 onwards',
            'category': 'Year Filtering',
            'query': 'Export papers from 2020 onwards to recent_2020.bib',
            'expected_range': (50, total),  # Flexible range
            'filename': 'recent_2020.bib'
        },
        {
            'name': 'Papers from 2023 onwards',
            'category': 'Year Filtering',
            'query': 'Export papers from 2023 onwards to very_recent.bib',
            'expected_range': (10, total),  # Flexible range
            'filename': 'very_recent.bib'
        },
        {
            'name': 'Papers from 2024',
            'category': 'Year Filtering',
            'query': 'Export papers from 2024 to papers_2024.bib',
            'expected_range': (0, total),  # Flexible range
            'filename': 'papers_2024.bib'
        },
        
        # ========== COMBINED FILTERS ==========
        {
            'name': 'Transformers from 2023+',
            'category': 'Combined Filters',
            'query': 'Export transformer papers from 2023 onwards to recent_transformers.bib',
            'expected_range': (1, keyword_counts.get('transformer', total)),
            'filename': 'recent_transformers.bib'
        },
        {
            'name': 'Recent surveys',
            'category': 'Combined Filters',
            'query': 'Export survey papers from 2022 onwards to recent_surveys.bib',
            'expected_range': (1, keyword_counts.get('survey', total)),
            'filename': 'recent_surveys.bib'
        },
        
        # ========== SOURCE FILTERING ==========
        {
            'name': 'ArXiv papers only',
            'category': 'Source Filtering',
            'query': 'Export only arxiv papers to arxiv_papers.bib',
            'expected_range': (db_stats['by_source'].get('arxiv', 0), db_stats['by_source'].get('arxiv', 0)),
            'filename': 'arxiv_papers.bib'
        },
        {
            'name': 'OpenAlex papers only',
            'category': 'Source Filtering',
            'query': 'Export only openalex papers to openalex_papers.bib',
            'expected_range': (db_stats['by_source'].get('openalex', 0), db_stats['by_source'].get('openalex', 0)),
            'filename': 'openalex_papers.bib'
        },
        
        # ========== EDGE CASES ==========
        {
            'name': 'Empty result (nonexistent keyword)',
            'category': 'Edge Cases',
            'query': 'Export papers about quantum_blockchain_ai_xyz to empty.bib',
            'expected_range': (0, 0),
            'filename': 'empty.bib'
        },
        {
            'name': 'Special characters in filename',
            'category': 'Edge Cases',
            'query': 'Export all papers to my_papers_2024.bib',
            'expected_range': (total, total),
            'filename': 'my_papers_2024.bib'
        },
    ]
    
    return test_cases


def main():
    """Run comprehensive evaluation"""
    print(f"{Color.BOLD}{Color.BLUE}")
    print("=" * 70)
    print("BibTeX Export Feature - Comprehensive Evaluation Suite")
    print("=" * 70)
    print(f"{Color.END}\n")
    
    evaluator = BibTeXEvaluator()
    evaluator.start_time = time.time()
    
    # Print database statistics
    evaluator.print_statistics()
    
    # Generate test cases
    test_cases = get_test_cases(evaluator.db_stats)
    
    print(f"\n{Color.BOLD}Generated {len(test_cases)} test cases{Color.END}")
    print(f"\nTest categories:")
    categories = set(t['category'] for t in test_cases)
    for cat in sorted(categories):
        count = sum(1 for t in test_cases if t['category'] == cat)
        print(f"  • {cat}: {count} tests")
    
    print(f"\n{Color.YELLOW}{'='*70}{Color.END}")
    print(f"{Color.BOLD}INSTRUCTIONS:{Color.END}")
    print(f"1. Run each test query in your main.py")
    print(f"2. The script will validate the output files")
    print(f"3. Results will be saved to JSON and text reports")
    print(f"{Color.YELLOW}{'='*70}{Color.END}")
    
    input(f"\n{Color.BOLD}Press Enter to start evaluation...{Color.END}\n")
    
    # Run all tests
    for test in test_cases:
        evaluator.run_test(
            test_name=test['name'],
            test_category=test['category'],
            query=test['query'],
            expected_range=test['expected_range'],
            filename=test['filename']
        )
        time.sleep(0.5)  # Brief pause between tests
    
    # Print summary
    evaluator.print_summary()
    
    # Save results
    evaluator.save_results()
    
    print(f"\n{Color.GREEN}{Color.BOLD}✓ Evaluation complete!{Color.END}")
    print(f"\nTest outputs saved to: {evaluator.test_dir}/")
    print(f"Results saved to: bibtex_evaluation_results.json")
    print(f"Report saved to: bibtex_evaluation_report.txt")


if __name__ == "__main__":
    main()

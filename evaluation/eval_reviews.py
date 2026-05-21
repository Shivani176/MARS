"""
Literature Review Evaluation Script
Clean metrics-only evaluation
"""

import os
import re
import sqlite3
import pandas as pd
from pathlib import Path
from collections import defaultdict

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_PATH = r"C:\AI_Agent_draft\evaluation_reviews"
DATABASE_PATH = r"C:\AI_Agent_draft\papers.db"

SYSTEMS = {
    'MySystem': 'Your System',
    'Elicit': 'Elicit',
    'Consensus': 'Consensus'
}

# Query topics for database search
QUERY_TOPICS = {
    'Q01': 'BERT',
    'Q02': 'GPT',
    'Q03': 'transformer',
    'Q04': 'natural language processing',
    'Q05': 'vision transformer',
    'Q06': 'CNN',
    'Q07': 'image segmentation',
    'Q08': 'computer vision',
    'Q09': 'attention mechanism',
    'Q10': 'transfer learning',
    'Q11': 'neural networks',
    'Q12': 'deep learning',
    'Q13': 'graph neural networks',
    'Q14': 'GAN',
    'Q15': 'neural architecture search'
}

# ============================================================================
# CITATION EXTRACTION
# ============================================================================

def extract_citations_mysystem(text):
    """Extract ALL citations from Your System reviews"""
    citations = re.findall(r'\[(\d+)\]', text)
    comma_citations = re.findall(r'\[(\d+(?:,\s*\d+)*)\]', text)
    for citation_group in comma_citations:
        citations.extend(citation_group.split(','))
    citations = [c.strip() for c in citations]
    unique_citations = list(set(citations))
    return citations, unique_citations

def extract_citations_elicit(text):
    """Extract citations from Elicit"""
    citations = []
    pattern1 = re.findall(r'<citations>(\d+)</citations>', text)
    citations.extend(pattern1)
    pattern2 = re.findall(r'\[(\d+)\]', text)
    citations.extend(pattern2)
    if 'Reference' in text or 'Citation' in text:
        refs_section = text.split('Reference')[-1] if 'Reference' in text else text.split('Citation')[-1]
        numbered = re.findall(r'^(\d+)\.', refs_section, re.MULTILINE)
        citations.extend(numbered)
    unique_citations = list(set(citations))
    return citations, unique_citations

def extract_citations_consensus(text):
    """Extract citations from Consensus"""
    citations = []
    pattern1 = re.findall(
        r'\([A-ZÀ-Ž][A-Za-zÀ-žçñ\'\-]+(?:\s+[A-ZÀ-Ž][A-Za-zÀ-žçñ\'\-]+)*'
        r'(?:\s+et\s+al\.)?'
        r'(?:,?\s+\d{4}[a-z]?)\)',
        text
    )
    citations.extend(pattern1)
    pattern2 = re.findall(
        r'\([A-ZÀ-Ž][A-Za-zÀ-žçñ\'\-]+(?:,\s+[A-ZÀ-Ž][A-Za-zÀ-žçñ\'\-]+)*'
        r'(?:\s+&\s+[A-ZÀ-Ž][A-Za-zÀ-žçñ\'\-]+)?'
        r',\s+\d{4}[a-z]?\)',
        text
    )
    citations.extend(pattern2)
    if 'References' in text or 'REFERENCES' in text:
        refs = text.split('References')[-1] if 'References' in text else text.split('REFERENCES')[-1]
        ref_lines = [line for line in refs.split('\n') if len(line.strip()) > 20]
        actual_refs = [line for line in ref_lines if re.search(r'\d{4}', line) and re.search(r'[A-Z][a-z]+', line)]
        if len(actual_refs) > len(citations):
            citations = actual_refs
    unique_citations = list(set(citations))
    return citations, unique_citations

def count_citations(text, system):
    """Main citation counting function"""
    if system == 'MySystem':
        total, unique = extract_citations_mysystem(text)
    elif system == 'Elicit':
        total, unique = extract_citations_elicit(text)
    elif system == 'Consensus':
        total, unique = extract_citations_consensus(text)
    else:
        total, unique = [], []
    return len(total), len(unique)

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

def get_papers_found_for_query(query_topic, db_path):
    """Search database to find how many papers exist for this query"""
    if not os.path.exists(db_path):
        print(f"Warning: Database not found: {db_path}")
        return 100
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = f"%{query_topic}%"
        cursor.execute("""
            SELECT COUNT(*)
            FROM papers
            WHERE (LOWER(title) LIKE LOWER(?) OR LOWER(abstract) LIKE LOWER(?))
            AND abstract IS NOT NULL
        """, (query, query))
        count = cursor.fetchone()[0]
        conn.close()
        return max(10, min(count, 100))
    except Exception as e:
        print(f"Database error for '{query_topic}': {e}")
        return 100

# ============================================================================
# METRICS CALCULATION
# ============================================================================

def calculate_basic_metrics(text, system):
    """Calculate length, citations, etc."""
    text_no_refs = text
    for separator in ['References', 'REFERENCES', '## References', 'Bibliography']:
        if separator in text:
            text_no_refs = text.split(separator)[0]
            break
    length = len(text_no_refs)
    word_count = len(text_no_refs.split())
    total_citations, unique_citations = count_citations(text, system)
    sections = len(re.findall(r'^#{1,3}\s+.*$|^\d+\.\s+[A-Z]', text, re.MULTILINE))
    sections = max(sections, 1)
    return {
        'length': length,
        'word_count': word_count,
        'total_citations': total_citations,
        'unique_citations': unique_citations,
        'sections': sections
    }

def calculate_citation_density(total_citations, length):
    """Citations per 1000 characters"""
    if length == 0:
        return 0
    return (total_citations / length) * 1000

def calculate_coverage(unique_citations, papers_found):
    """Coverage = unique papers cited / papers found for query"""
    if papers_found == 0:
        return 0
    coverage = unique_citations / papers_found
    return min(coverage, 1.0)

def calculate_quality_score(coverage, density, length):
    """
    Quality Score Formula
    Quality = 0.5 × Coverage + 0.3 × Density_norm + 0.2 × Length_norm
    """
    # Density normalization
    if density < 3:
        density_norm = density / 3.0
    elif density <= 6:
        density_norm = 1.0
    elif density <= 15:
        density_norm = 0.7
    elif density <= 20:
        penalty = (density - 15) / 5
        density_norm = 0.7 - (penalty * 0.4)
    else:
        density_norm = 0.3
    
    density_norm = max(0, min(1, density_norm))
    
    # Normalize length
    length_norm = min(length / 10000, 1.0)
    
    # Calculate final quality score
    quality = (0.5 * coverage) + (0.3 * density_norm) + (0.2 * length_norm)
    
    return quality, density_norm

# ============================================================================
# FILE I/O
# ============================================================================

def read_file(filepath):
    """Read file with encoding handling"""
    for encoding in ['utf-8', 'latin-1', 'cp1252']:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except:
            continue
    return ""

# ============================================================================
# MAIN EVALUATION
# ============================================================================

def evaluate_all_reviews():
    """Main evaluation function"""
    
    print("="*80)
    print("LITERATURE REVIEW EVALUATION")
    print("="*80)
    print("\nEvaluating system performance using objective metrics")
    
    # Get paper counts
    print("\nGetting paper counts from database...")
    papers_found = {}
    for query_id, topic in QUERY_TOPICS.items():
        count = get_papers_found_for_query(topic, DATABASE_PATH)
        papers_found[query_id] = count
        print(f"  {query_id} ({topic}): {count} papers found")
    
    results = []
    
    # Process each system
    for system_folder, system_name in SYSTEMS.items():
        print(f"\nProcessing {system_name}...")
        
        system_path = os.path.join(BASE_PATH, system_folder)
        
        if not os.path.exists(system_path):
            print(f"  Error: {system_path} not found")
            continue
        
        files = os.listdir(system_path)
        
        # Process each query
        for query_id, topic in QUERY_TOPICS.items():
            
            # Find matching file
            matching_file = None
            for filename in files:
                if query_id in filename:
                    matching_file = filename
                    break
            
            if not matching_file:
                print(f"  Warning: No file for {query_id}")
                continue
            
            filepath = os.path.join(system_path, matching_file)
            text = read_file(filepath)
            
            if not text:
                print(f"  Warning: Could not read {matching_file}")
                continue
            
            # Calculate metrics
            basic = calculate_basic_metrics(text, system_folder)
            density = calculate_citation_density(basic['total_citations'], basic['length'])
            
            # Calculate coverage
            papers_for_query = papers_found.get(query_id, 100)
            coverage = calculate_coverage(basic['unique_citations'], papers_for_query)
            
            # Quality score
            quality, density_norm = calculate_quality_score(coverage, density, basic['length'])
            
            # Store results
            results.append({
                'System': system_name,
                'Query_ID': query_id,
                'Query': topic,
                'Length': basic['length'],
                'Words': basic['word_count'],
                'Total_Citations': basic['total_citations'],
                'Unique_Citations': basic['unique_citations'],
                'Papers_Found': papers_for_query,
                'Coverage_%': round(coverage * 100, 1),
                'Density': round(density, 2),
                'Density_Norm': round(density_norm, 2),
                'Quality_Score': round(quality, 3),
                'Filename': matching_file
            })
            
            print(f"  ✓ {query_id}: Quality={quality:.2f}, Coverage={coverage*100:.0f}%")
    
    # Convert to DataFrame
    df = pd.DataFrame(results)
    
    # Save
    df.to_csv('evaluation_results.csv', index=False)
    print(f"\n✓ Results saved to: evaluation_results.csv")
    
    # Generate summaries
    generate_summary(df)
    generate_comparison_tables(df)
    
    return df

def generate_summary(df):
    """Summary statistics"""
    
    print("\n" + "="*80)
    print("SUMMARY BY SYSTEM")
    print("="*80)
    
    summary = df.groupby('System').agg({
        'Length': 'mean',
        'Words': 'mean',
        'Total_Citations': 'mean',
        'Unique_Citations': 'mean',
        'Coverage_%': 'mean',
        'Density': 'mean',
        'Density_Norm': 'mean',
        'Quality_Score': 'mean'
    }).round(2)
    
    print(summary)
    
    # Calculate performance metrics
    print("\n" + "="*80)
    print("PERFORMANCE METRICS")
    print("="*80)
    
    for system in df['System'].unique():
        system_df = df[df['System'] == system]
        print(f"\n{system}:")
        print(f"  Quality Score: {system_df['Quality_Score'].mean():.3f} ± {system_df['Quality_Score'].std():.3f}")
        print(f"  Coverage Range: {system_df['Coverage_%'].min():.1f}% - {system_df['Coverage_%'].max():.1f}%")
        print(f"  Median Quality: {system_df['Quality_Score'].median():.3f}")
        
        # Count high-quality reviews (quality > 0.6)
        high_quality = len(system_df[system_df['Quality_Score'] > 0.6])
        print(f"  High-Quality Reviews (>0.6): {high_quality}/15 ({high_quality/15*100:.0f}%)")
    
    summary.to_csv('evaluation_summary.csv')

def generate_comparison_tables(df):
    """Comparison tables"""
    
    print("\n" + "="*80)
    print("SYSTEM COMPARISON")
    print("="*80)
    
    comparison = df.groupby('System').agg({
        'Quality_Score': 'mean',
        'Coverage_%': 'mean',
        'Length': 'mean',
        'Total_Citations': 'mean',
        'Unique_Citations': 'mean',
        'Density': 'mean',
        'Density_Norm': 'mean'
    }).round(2)
    
    print(comparison)
    
    comparison.to_csv('system_comparison.csv')
    
    print("\n✓ All files saved")

# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    print("Starting evaluation...\n")
    
    if not os.path.exists(BASE_PATH):
        print(f"ERROR: {BASE_PATH} not found")
        exit(1)
    
    df = evaluate_all_reviews()
    
    print("\n" + "="*80)
    print("EVALUATION COMPLETE!")
    print("="*80)
    print("\nFiles created:")
    print("  - evaluation_results.csv")
    print("  - evaluation_summary.csv")
    print("  - system_comparison.csv")
    print("="*80)
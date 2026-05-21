"""
DATABASE TOPIC ANALYSIS
Analyzes your 615 papers to find major CS domains and topics

This will show you:
1. Most common keywords in titles
2. Topic clusters (what domains you have)
3. Papers per topic
4. Suggested queries for evaluation
"""

import sqlite3
import json
from collections import Counter
import re

print("="*80)
print("DATABASE TOPIC ANALYSIS")
print("="*80)

# Connect to database
conn = sqlite3.connect("papers.db")
cursor = conn.cursor()

# Get all papers
cursor.execute("SELECT title, abstract, year, source FROM papers")
papers = cursor.fetchall()

print(f"\nTotal papers in database: {len(papers)}")
print(f"Analyzing {len(papers)} papers...\n")

# ============================================================
# PART 1: KEYWORD FREQUENCY ANALYSIS
# ============================================================

print("="*80)
print("PART 1: MOST COMMON KEYWORDS IN TITLES")
print("="*80)

# Common stop words to ignore
stop_words = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
    'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'must', 'can', 'about', 'into', 'through',
    'using', 'via', 'based', 'new', 'novel', 'approach', 'towards', 'toward'
}

# Extract all words from titles
all_words = []
for title, _, _, _ in papers:
    if title:
        # Clean and split title
        words = re.findall(r'\b[a-z]{3,}\b', title.lower())
        # Filter out stop words
        words = [w for w in words if w not in stop_words]
        all_words.extend(words)

# Count frequency
word_freq = Counter(all_words)

print("\nTop 50 Keywords (single words):")
print(f"{'Rank':<6} {'Keyword':<20} {'Count':<8} {'% of Papers'}")
print("-"*60)

for i, (word, count) in enumerate(word_freq.most_common(50), 1):
    percentage = (count / len(papers)) * 100
    print(f"{i:<6} {word:<20} {count:<8} {percentage:>5.1f}%")

# ============================================================
# PART 2: BIGRAM ANALYSIS (Two-word phrases)
# ============================================================

print("\n" + "="*80)
print("PART 2: MOST COMMON TWO-WORD PHRASES")
print("="*80)

bigrams = []
for title, _, _, _ in papers:
    if title:
        words = re.findall(r'\b[a-z]{3,}\b', title.lower())
        words = [w for w in words if w not in stop_words]
        # Create bigrams
        for i in range(len(words) - 1):
            bigrams.append(f"{words[i]} {words[i+1]}")

bigram_freq = Counter(bigrams)

print("\nTop 30 Two-Word Phrases:")
print(f"{'Rank':<6} {'Phrase':<30} {'Count':<8} {'% of Papers'}")
print("-"*70)

for i, (phrase, count) in enumerate(bigram_freq.most_common(30), 1):
    percentage = (count / len(papers)) * 100
    print(f"{i:<6} {phrase:<30} {count:<8} {percentage:>5.1f}%")

# ============================================================
# PART 3: DOMAIN CLASSIFICATION (CS Subfields)
# ============================================================

print("\n" + "="*80)
print("PART 3: CS DOMAIN COVERAGE")
print("="*80)

# Define domain keywords
domains = {
    'Natural Language Processing': [
        'bert', 'gpt', 'nlp', 'language', 'transformer', 'translation',
        'text', 'sentiment', 'question', 'answer', 'chatbot', 'dialogue',
        'speech', 'named', 'entity', 'pos', 'tagging', 'parsing'
    ],
    'Computer Vision': [
        'image', 'vision', 'detection', 'segmentation', 'object', 'visual',
        'cnn', 'convolutional', 'resnet', 'yolo', 'recognition', 'classification',
        'video', 'face', 'scene', 'pixel'
    ],
    'Deep Learning / Neural Networks': [
        'neural', 'network', 'deep', 'learning', 'training', 'optimization',
        'gradient', 'backpropagation', 'layer', 'activation', 'loss',
        'embedding', 'attention', 'feedforward', 'recurrent', 'lstm', 'gru'
    ],
    'Machine Learning': [
        'machine', 'learning', 'supervised', 'unsupervised', 'classification',
        'regression', 'clustering', 'reinforcement', 'algorithm', 'model',
        'prediction', 'feature', 'training', 'validation'
    ],
    'Medical / Healthcare AI': [
        'medical', 'health', 'disease', 'diagnosis', 'patient', 'clinical',
        'radiology', 'biomedical', 'cancer', 'mri', 'ct', 'scan', 'drug'
    ],
    'Robotics / Control': [
        'robot', 'robotics', 'control', 'manipulation', 'grasp', 'slam',
        'navigation', 'autonomous', 'motion', 'planning', 'trajectory'
    ],
    'Transformers / Attention': [
        'transformer', 'attention', 'self-attention', 'multi-head', 'bert',
        'gpt', 'positional', 'encoding', 'query', 'key', 'value'
    ],
    'Generative Models': [
        'gan', 'generative', 'adversarial', 'vae', 'diffusion', 'generation',
        'synthesis', 'autoencoder', 'latent'
    ],
}

domain_counts = {}

for domain, keywords in domains.items():
    count = 0
    for title, abstract, _, _ in papers:
        text = (title or '').lower() + ' ' + (abstract or '').lower()
        if any(keyword in text for keyword in keywords):
            count += 1
    domain_counts[domain] = count

# Sort by count
sorted_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)

print("\nPapers by CS Domain (papers may appear in multiple domains):")
print(f"{'Domain':<40} {'Papers':<10} {'Coverage'}")
print("-"*70)

for domain, count in sorted_domains:
    percentage = (count / len(papers)) * 100
    bar = "█" * int(percentage / 2)
    print(f"{domain:<40} {count:<10} {bar} {percentage:.1f}%")

# ============================================================
# PART 4: SPECIFIC TOPICS / ARCHITECTURES
# ============================================================

print("\n" + "="*80)
print("PART 4: SPECIFIC MODELS / ARCHITECTURES")
print("="*80)

specific_topics = {
    'BERT': ['bert'],
    'GPT': ['gpt'],
    'Transformer': ['transformer'],
    'ResNet': ['resnet', 'residual network'],
    'CNN': ['cnn', 'convolutional neural'],
    'LSTM': ['lstm', 'long short-term'],
    'GAN': ['gan', 'generative adversarial'],
    'Attention Mechanism': ['attention mechanism', 'self-attention', 'multi-head attention'],
    'Vision Transformer (ViT)': ['vision transformer', 'vit'],
    'Object Detection': ['object detection', 'yolo', 'faster r-cnn', 'rcnn'],
    'Image Segmentation': ['segmentation', 'semantic segmentation', 'instance segmentation'],
    'Transfer Learning': ['transfer learning', 'fine-tuning', 'pretrain'],
    'Reinforcement Learning': ['reinforcement learning', 'q-learning', 'policy gradient'],
    'Medical Imaging': ['medical image', 'medical imaging', 'radiology'],
    'Neural Architecture Search': ['nas', 'architecture search', 'automl'],
}

topic_counts = {}

for topic, keywords in specific_topics.items():
    count = 0
    for title, abstract, _, _ in papers:
        text = (title or '').lower() + ' ' + (abstract or '').lower()
        if any(keyword in text for keyword in keywords):
            count += 1
    topic_counts[topic] = count

# Sort by count
sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)

print("\nPapers by Specific Topic:")
print(f"{'Topic':<35} {'Papers':<10} {'Suitable for Eval?'}")
print("-"*70)

for topic, count in sorted_topics:
    if count >= 20:
        status = "✅ YES (20+ papers)"
    elif count >= 10:
        status = "⚠️  MAYBE (10-19 papers)"
    else:
        status = "❌ NO (<10 papers)"
    
    print(f"{topic:<35} {count:<10} {status}")

# ============================================================
# PART 5: SUGGESTED QUERIES FOR EVALUATION
# ============================================================

print("\n" + "="*80)
print("PART 5: SUGGESTED QUERIES FOR YOUR EVALUATION")
print("="*80)

# Get topics with 15+ papers
good_topics = [(topic, count) for topic, count in sorted_topics if count >= 15]

print(f"\nTopics with 15+ papers (suitable for evaluation):")
print(f"Found {len(good_topics)} suitable topics\n")

if len(good_topics) >= 20:
    print("✅ You have 20+ topics with good coverage!")
    print("\nSuggested 20 queries for evaluation:")
    print("-"*70)
    for i, (topic, count) in enumerate(good_topics[:20], 1):
        print(f"{i:>2}. {topic:<35} ({count} papers)")
else:
    print(f"⚠️  You have {len(good_topics)} topics with 15+ papers.")
    print("Need to either:")
    print("  1. Lower threshold to 10+ papers, OR")
    print("  2. Add more papers to reach 20 topics, OR")
    print("  3. Use broader queries")
    
    print("\nAll available topics (10+ papers):")
    print("-"*70)
    marginal_topics = [(topic, count) for topic, count in sorted_topics if 10 <= count < 15]
    all_usable = good_topics + marginal_topics
    
    for i, (topic, count) in enumerate(all_usable[:25], 1):
        status = "✅" if count >= 15 else "⚠️ "
        print(f"{i:>2}. {status} {topic:<33} ({count} papers)")

# ============================================================
# PART 6: SOURCE DISTRIBUTION
# ============================================================

print("\n" + "="*80)
print("PART 6: SOURCE DISTRIBUTION")
print("="*80)

cursor.execute("SELECT source, COUNT(*) FROM papers GROUP BY source")
sources = cursor.fetchall()

print("\nPapers by source:")
for source, count in sources:
    percentage = (count / len(papers)) * 100
    print(f"  {source}: {count} papers ({percentage:.1f}%)")

# ============================================================
# PART 7: YEAR DISTRIBUTION
# ============================================================

print("\n" + "="*80)
print("PART 7: YEAR DISTRIBUTION")
print("="*80)

cursor.execute("SELECT year, COUNT(*) FROM papers WHERE year IS NOT NULL GROUP BY year ORDER BY year DESC")
years = cursor.fetchall()

print("\nPapers by year:")
for year, count in years[:10]:  # Show last 10 years
    percentage = (count / len(papers)) * 100
    bar = "█" * int(count / 5)
    print(f"  {year}: {bar} {count} papers ({percentage:.1f}%)")

conn.close()

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print("\nNext steps:")
print("1. Review the suggested queries above")
print("2. Pick 20 queries from topics with good coverage (15+ papers)")
print("3. Apply the hybrid_search fix")
print("4. Validate queries return appropriate paper counts")
print("="*80)
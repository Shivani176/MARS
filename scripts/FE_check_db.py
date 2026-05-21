from tools import PaperDatabase
from memory_manager import MemoryManager

db = PaperDatabase()
memory = MemoryManager()

# Get total count
import sqlite3
conn = sqlite3.connect("papers.db")
cursor = conn.cursor()
print("connected papers.db")

# Total papers
cursor.execute("SELECT COUNT(*) FROM papers")
total = cursor.fetchone()[0]

print("total papers:   SELECT COUNT(*) FROM papers")

# Papers with abstracts (needed for hybrid search)
cursor.execute("SELECT COUNT(*) FROM papers WHERE abstract IS NOT NULL AND abstract != ''")
with_abstract = cursor.fetchone()[0]



# Papers by source
cursor.execute("""
    SELECT source, COUNT(*) as count 
    FROM papers 
    GROUP BY source 
    ORDER BY count DESC
""")
sources = cursor.fetchall()

conn.close()

print("="*60)
print("DATABASE SUMMARY")
print("="*60)
print(f"Total papers: {total}")
print(f"Papers with abstracts: {with_abstract}")
print(f"\nBreakdown by source:")
for source, count in sources:
    print(f"  {source}: {count}")
print("="*60)
#!/usr/bin/env python3
"""Create initial index.json from existing book data files."""

from books import Review
import glob
import json
from pathlib import Path
import datetime as dt

INDEX_FILE = Path('./data/index.json')

def create_index():
    """Build index from all existing book files."""
    index = {}
    
    # Glob for all review and to-read files
    review_files = glob.glob('./data/reviews/**/index.md', recursive=True)
    to_read_files = glob.glob('./data/to-read/**/index.md', recursive=True)
    
    all_files = review_files + to_read_files
    
    print(f"Found {len(all_files)} book files to index...")
    
    for filepath in all_files:
        try:
            r = Review(path=filepath)
            isbn13 = r.metadata.get('book', {}).get('isbn13')
            title = r.metadata.get('book', {}).get('title', 'Unknown')
            
            # Determine entry type from path
            if 'reviews' in filepath:
                entry_type = 'reviews'
            elif 'to-read' in filepath:
                entry_type = 'to-read'
            else:
                entry_type = 'unknown'
            
            if isbn13:
                # Get date_read from review metadata
                date_read = r.metadata.get('review', {}).get('date_read')
                if isinstance(date_read, list) and date_read:
                    date_read = date_read[0]
                if date_read is None:
                    date_read = dt.date.today().isoformat()
                elif not isinstance(date_read, str):
                    date_read = str(date_read)
                
                index[isbn13] = {
                    'title': title,
                    'type': entry_type,
                    'added': date_read
                }
                print(f"  ✓ {title}")
            else:
                print(f"  ⚠ Skipped (no ISBN): {title}")
        except Exception as e:
            print(f"  ✗ Error reading {filepath}: {e}")
    
    # Write index file
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, 'w') as f:
        json.dump(index, f, indent=2)
    
    print(f"\nIndex created: {INDEX_FILE}")
    print(f"Total entries: {len(index)}")

if __name__ == "__main__":
    create_index()

import json
import os
from datetime import datetime
from app import app, db
from models import Post

def import_data():
    # VERY IMPORTANT: This script should ONLY be run when DATABASE_URL is set to the Neon DB
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("ERROR: DATABASE_URL environment variable is not set.")
        print("Please set it to your Neon PostgreSQL connection string before running this script.")
        print("Example (Windows): set DATABASE_URL=postgresql://user:pass@ep-rest-of-url.neon.tech/neondb")
        return

    # Check that it's actually connecting to Postgres and not local SQLite
    if not db_url.startswith('postgre'):
        print("WARNING: DATABASE_URL doesn't look like a PostgreSQL URL.")
        confirm = input("Are you sure you want to proceed? (y/n): ")
        if confirm.lower() != 'y':
            print("Import cancelled.")
            return

    try:
        with open('local_data_export.json', 'r') as f:
            post_data = json.load(f)
    except FileNotFoundError:
        print("ERROR: 'local_data_export.json' not found. Please run export_db.py first.")
        return

    with app.app_context():
        print(f"Connected to database at {db_url}")
        
        # Ensure tables exist
        db.create_all()
        
        imported_count = 0
        skipped_count = 0
        
        for p_data in post_data:
            # Check if post already exists
            existing_post = Post.query.filter_by(slug=p_data['slug']).first()
            if existing_post:
                print(f"Skipping existing post: {p_data['title']}")
                skipped_count += 1
                continue
                
            # Parse datetime
            date_posted = None
            if p_data['date_posted']:
                try:
                    date_posted = datetime.fromisoformat(p_data['date_posted'])
                except ValueError:
                    date_posted = datetime.utcnow()
            else:
                date_posted = datetime.utcnow()
                
            post = Post(
                title=p_data['title'],
                slug=p_data['slug'],
                summary=p_data['summary'],
                content=p_data['content'],
                category=p_data['category'],
                author=p_data.get('author'),
                image_url=p_data['image_url'],
                date_posted=date_posted,
                is_published=p_data.get('is_published', True),
                views=p_data.get('views', 0)
            )
            db.session.add(post)
            imported_count += 1
            
        db.session.commit()
        print(f"\nImport Summary:")
        print(f"- Imported: {imported_count} posts")
        print(f"- Skipped: {skipped_count} posts (already exist)")
        print("\nData migration complete!")

if __name__ == '__main__':
    import_data()

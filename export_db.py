import json
from app import app, db
from models import Post

def export_data():
    with app.app_context():
        # Get all posts from the local SQLite database
        posts = Post.query.all()
        
        # Convert posts to a list of dictionaries
        post_data = []
        for post in posts:
            post_dict = {
                'title': post.title,
                'slug': post.slug,
                'summary': post.summary,
                'content': post.content,
                'category': post.category,
                'author': post.author,
                'image_url': post.image_url,
                'date_posted': post.date_posted.isoformat() if post.date_posted else None,
                'is_published': post.is_published,
                'views': post.views
            }
            post_data.append(post_dict)
            
        # Write to JSON file
        with open('local_data_export.json', 'w') as f:
            json.dump(post_data, f, indent=4)
            
        print(f"Successfully exported {len(post_data)} posts to 'local_data_export.json'")

if __name__ == '__main__':
    export_data()

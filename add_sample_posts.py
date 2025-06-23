import sqlite3

# Connect to your blog.db
conn = sqlite3.connect('blog.db')
cursor = conn.cursor()

# Sample posts
sample_posts = [
    ("Welcome to My Blog", "This is my first post. Excited to share more!"),
    ("Learning Flask", "Flask is a lightweight web framework in Python. I’m enjoying building with it."),
    ("Deploying with Render", "Render makes it easy to deploy full-stack apps for free."),
]

# Insert posts
cursor.executemany('INSERT INTO posts (title, content) VALUES (?, ?)', sample_posts)

conn.commit()
conn.close()

print("Sample blog posts added successfully!")

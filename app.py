from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # ← use any long random string



# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Sudu9008@#',  # ← change this
        database='flask_blog'
    )

@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts ORDER BY id DESC')
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('home.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'user' not in session:
        return redirect(url_for('login'))  # 👈 Block if not logged in
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO posts (title, content) VALUES (%s, %s)', (title, content))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('home'))

    return render_template('create.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simple fixed credentials (for now)
        if username == 'admin' and password == 'password':
            session['user'] = username
            return redirect(url_for('create'))
        else:
            flash('Invalid credentials')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute('UPDATE posts SET title=%s, content=%s WHERE id=%s', (title, content, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('home'))

    cursor.execute('SELECT * FROM posts WHERE id=%s', (id,))
    post = cursor.fetchone()
    cursor.close()
    conn.close()

    if post:
        return render_template('edit.html', post=post)
    else:
        return 'Post not found', 404
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM posts WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)


   


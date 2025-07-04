from flask import Flask, render_template, abort, request, redirect, url_for, jsonify
import sqlite3

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/', methods=['GET'])
def base():
    return render_template('base.html')

@app.route('/home', methods=['GET'])
def home():
    titulo = "esta es el html home como variable"
    return render_template('home.html', titulo=titulo)

@app.route('/posts', methods=['GET'])
def get_all_posts():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('post/post_list.html', posts=posts)


@app.route('/posts/<int:post_id>', methods=['GET'])
def get_one_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return render_template("post/post.html", post=post)

@app.route('/posts/create', methods=['GET', 'POST'])
def create_one_post():
    if request.method == "GET":
        return render_template("post/create.html")
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('get_all_posts'))
    

@app.route('/posts/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_one_post(post_id):
    if request.method == "GET":
        conn = get_db_connection()
        post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
        conn.close()
        return render_template("post/edit.html", post=post)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        conn = get_db_connection()
        conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, post_id))
        conn.commit()
        conn.close()
        return redirect(url_for('get_all_posts'))
    

@app.route('/posts/delete/<int:post_id>', methods=['DELETE'])
def delete_one_post(post_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    return "", 200


@app.route('/api/new', methods=['GET'])
def new():
    datos = [
        {
        "nombre": "Jorge",
        "edad": 35,
        "trabaja": True
        },
        {
        "nombre": "Jaime",
        "edad": 34,
        "trabaja": False
        },
    ]
    return datos, 200

if __name__ == '__main__':
    app.run(debug=True)
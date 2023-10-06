from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from user2 import db as user_db, User
from post2 import db as post_db, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Debug toolbar
toolbar = DebugToolbarExtension(app)

# Initialize databases
user_db.init_app(app)
post_db.init_app(app)

# Homepage redirects to list of all users
@app.route('/')
def root():
    return redirect("/users")

# Shows page with info of all users
@app.route('/users')
def users_index():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index2.html', users=users)

# Form to create a new user
@app.route('/users/new', methods=["GET"])
def users_new_form():
    return render_template('users/new2.html')

# Create a new user
@app.route("/users/new", methods=["POST"])
def users_new():
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None
    )
    
    user_db.session.add(new_user)
    user_db.session.commit()

    return redirect("/users")

# User profile page
@app.route('/users/<int:user_id>')
def users_show(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('users/show2.html', user=user, posts=posts)

# Edit User form
@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/edit2.html', user=user)

# Submission form for updating user
@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    user =  User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    user_db.session.commit()

    return redirect("/users")

# Delete existing user
@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    user = User.query.get_or_404(user_id)
    user_db.session.delete(user)
    user_db.session.commit()

    return redirect("/users")

# Show form to add a post for a specific user
@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def posts_new_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('posts/new2.html', user=user)

# Handle add form; add post and redirect to the user detail page
@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    user = User.query.get_or_404(user_id)
    new_post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user=user
    )
    
    post_db.session.add(new_post)
    post_db.session.commit()

    return redirect(f"/users/{user_id}")

# Show a post and buttons to edit and delete the post
@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/show2.html', post=post)

# Show form to edit a post
@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit2.html', post=post)

# Handle editing of a post
@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    post_db.session.commit()

    return redirect(f"/posts/{post_id}")

# Delete a post
@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    post = Post.query.get_or_404(post_id)
    post_db.session.delete(post)
    post_db.session.commit()

    return redirect(f"/users/{post.user_id}")

if __name__ == '__main__':
    app.run(debug=True)

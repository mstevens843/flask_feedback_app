from flask import Flask, render_template, redirect, flash, session
from models import db, User, bcrypt, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '61a4771171c7b4122f0538191883406922df8cab72bc69cbff81619cb68deece'

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()


# ROUTES ##########################
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # Register the user (email removed)
        new_user = User.register(username, password, first_name, last_name)
        db.session.commit()

        # Store the username in the session
        session['username'] = new_user.username

        # Redirect to /users/<username>
        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Authenticate the user
        user = User.authenticate(username, password)

        if user:
            # Store the username in the session
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            flash('Invalid credentials, please try again.', 'danger')

    return render_template('login.html', form=form)


@app.route('/users/<username>')
def show_user(username):
    # Check if the user is logged in
    if "username" not in session or session['username'] != username:
        flash("You are not authorized to view this page.", "danger")
        return redirect('/login')

    # Fetch the user and their feedback
    user = User.query.get_or_404(username)
    feedback = Feedback.query.filter_by(username=username).all()

    return render_template('user_details.html', user=user, feedback=feedback)


# Logout functionality
@app.route('/logout')
def logout():
    # Clear session data
    session.pop('username', None)
    flash("You have been logged out.", "success")
    return redirect('/')


# GET /secret. Display secret message.
@app.route('/secret')
def secret():
    if "username" not in session:
        flash("You must be logged in to view this page", "danger")
        return redirect('/login')

    return "You made it"


# FEEDBACK ROUTES ##########################
@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    # Ensure the user is logged in and authorized
    if "username" not in session or session['username'] != username:
        flash("You are not authorized to perform this action.", "danger")
        return redirect('/login')

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        # Add feedback to the database
        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()

        flash("Feedback added successfully!", "success")
        return redirect(f'/users/{username}')

    return render_template('add_feedback.html', form=form)


@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    # Ensure the user is logged in and authorized
    if "username" not in session or session['username'] != feedback.username:
        flash("You are not authorized to perform this action.", "danger")
        return redirect('/login')

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()

        flash("Feedback updated successfully!", "success")
        return redirect(f'/users/{feedback.username}')

    return render_template('edit_feedback.html', form=form, feedback=feedback)


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    # Ensure the user is logged in and authorized
    if "username" not in session or session['username'] != feedback.username:
        flash("You are not authorized to perform this action.", "danger")
        return redirect('/login')

    db.session.delete(feedback)
    db.session.commit()

    flash("Feedback deleted successfully!", "success")
    return redirect(f'/users/{feedback.username}')


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    # Ensure the user is logged in and authorized
    if "username" not in session or session['username'] != username:
        flash("You are not authorized to perform this action.", "danger")
        return redirect('/login')

    user = User.query.get_or_404(username)

    # Delete the user and their feedback
    db.session.delete(user)
    db.session.commit()

    session.pop('username', None)
    flash("User account and all feedback deleted.", "success")
    return redirect('/')

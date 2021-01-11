from flask import Flask, render_template, redirect,flash,session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'asfdsfds'

connect_db(app)
db.create_all()

@app.route('/')
def base():

    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def show_register():
    '''register a user and redirect to a page for users only'''

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username,password, email, first_name,last_name)
        db.session.add(user)
        db.session.commit()
        session['username'] = user.username
        return redirect(f'/users/{user.username}')
    else:
        return render_template('register.html', form=form)

@app.route('/login',methods=["GET","POST"])
def login_user():
   
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        
        user = User.authenticate(username, password)  
        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template('login.html',form=form)
    
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    '''logout and return to home page'''
    session.pop('username')
    return redirect('/')

@app.route('/users/<username>')
def user_details(username):
    '''show information about a user'''

    if 'username' not in session or username != ['username']:
        flash('must be logged in to view')
        

    user = User.query.get(username)
    form = DeleteForm()

    return render_template('/users.html',user=user,form=form)

@app.route('/users/<username>/delete',methods=['POST'])
def delete_user(username):
    '''delete a user'''
    if 'username' not in session or username != ['username']:
        flash('must be logged in to view')
        

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('username')

    return redirect('/login')

@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    '''add feedback to their profile'''
    if 'username' not in session or username != ['username']:
        flash('must be logged in to view')
        
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title,content=content,username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f'/users/{feedback.username}')
    else:
        return render_template('feedback.html',form=form)


@app.route('/feedback/<int:feedback_id>/update', methods=['GET','POST'])
def update_feedback(feedback_id):
    '''update feedback written by a specific user'''

    feedback = Feedback.query.get(feedback_id)
    
    if 'username' not in session or username != ['username']:
        flash('must be logged in to view')
        
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f'/users/{feedback.username}')
    
    return render_template('feedback_update.html',form=form,feedback=feeback)

    
@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    '''delete feedback from their account'''
    feedback = Feedback.query.get(feedback_id)

    if 'username' not in session:
        flash('must be logged in to view')

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()
    
    return redirect(f'/users/{feedback.username}')

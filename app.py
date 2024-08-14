import logging
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, make_response
from config import DevelopmentConfig
from models import db, User, Movie, MovieStats
from forms import SignupForm, LoginForm, ChangePlanForm
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from posthog import Posthog

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Initialize CSRF protection
csrf = CSRFProtect(app)

posthog = Posthog(project_api_key='phc_VJnSeuzLa91xwVOxMOkFyAoEVabYBVFge1MIlBxdFTw', host='https://us.i.posthog.com')

db.init_app(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def index():
    movies = Movie.query.all()
    response = make_response(render_template('index.html', movies=movies))
    response.delete_cookie('posthog_js')
    return response

@app.route('/movie/<int:movie_id>')
def movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template('movie.html', movie=movie)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        app.logger.debug(f"Form data received: {request.form}")
        plan = request.form.get('plan')
        app.logger.debug(f"Plan value: {plan}")
        
        if form.validate_on_submit() and plan in ['Free', 'Premium', 'Max-imal']:
            user = User(
                username=form.username.data,
                email=form.email.data,
                plan=plan
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            app.logger.debug(f"New user created: {user.username} with plan: {user.plan}")
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        else:
            if 'plan' not in request.form or not request.form['plan']:
                flash('Please select a plan.', 'error')
            app.logger.debug(f"Form validation failed. Errors: {form.errors}")
    
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=True)
        posthog.identify(user.email)
        posthog.capture(user.email, 'user_logged_in')
        flash('Welcome back!')
        
        next_page = request.args.get('next')
        return redirect(next_page or url_for('index'))
    
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        posthog.capture(current_user.email, 'user_logged_out')
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
@csrf.exempt  # Disable CSRF for this route
def search():
    query = request.form.get('query')
    posthog.capture('search', 'search_performed', {'query': query})
    return redirect(url_for('search_results', query=query))

@app.route('/search_results')
def search_results():
    query = request.args.get('query')
    movies = Movie.query.filter(Movie.title.like(f'%{query}%')).all()
    return render_template('search_results.html', query=query, movies=movies)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ChangePlanForm()  

    if form.validate_on_submit():
        new_plan = form.plan.data
        if new_plan:
            current_user.plan = new_plan
            db.session.commit()
            posthog.capture(current_user.email, 'plan_changed', {'new_plan': new_plan})
            flash('Your subscription plan has been updated!')
        else:
            flash('Please select a valid plan.', 'danger')
        return redirect(url_for('profile'))
    
    stats_week = [stat.to_dict() for stat in MovieStats.query.filter_by(user_id=current_user.id, time_frame='week').all()]
    stats_month = [stat.to_dict() for stat in MovieStats.query.filter_by(user_id=current_user.id, time_frame='month').all()]
    stats_year = [stat.to_dict() for stat in MovieStats.query.filter_by(user_id=current_user.id, time_frame='year').all()]
    
    return render_template('profile.html', user=current_user, form=form, stats_week=stats_week, stats_month=stats_month, stats_year=stats_year)


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        pass
    return render_template('settings.html', user=current_user)

@app.route('/change_plan', methods=['POST'])
@login_required
def change_plan():
    new_plan = request.form.get('plan')
    if new_plan:
        current_user.plan = new_plan
        db.session.commit()
        posthog.capture(current_user.email, 'plan_changed', {'new_plan': new_plan})
        flash('Your subscription plan has been updated!')
    else:
        flash('Please select a valid plan.', 'danger')
    return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(debug=True)

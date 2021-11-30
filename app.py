from flask import Flask,render_template,request,flash,redirect
from flask_login import login_user,logout_user, UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY']='qwertyuiopasdfghjklzxcvbnm'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fname = db.Column(db.String(80), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    money = db.Column(db.Integer, nullable=True)
    def __repr__(self):
        return '<User %r>' % self.email + self.password

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user =User.query.filter_by(email=email).first()
        if user and password==user.password:
            login_user(user, remember=True)
            flash(f'Welcome to back AV7BANK {email}', 'success')
            return redirect('/')
        else:
            flash(f'Invalid Credentials."', 'warning')
            return redirect('/login')
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        fname = request.form.get('first_name')
        lname = request.form.get('last_name')
        user=User(email=email,password=password,fname=fname,lname=lname,money=0)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome to AV7BANK {email}', 'success')
        return redirect('/login')

    return render_template('register.html')

@app.route('/take_money', methods=['POST', 'GET'])
def takeMoney():
    if request.method=='POST':
        email = request.form.get("email")
        password = request.form.get("password")
        moneyTaken = request.form.get('value', type=int)
        print(moneyTaken)
        print(type(moneyTaken))
        user=User.query.filter_by(email=email).first()
        if user.password == password and moneyTaken < user.money:
            user.money = user.money-moneyTaken
            db.session.commit()
            flash('Money Taken from your account.', 'success')
            return redirect('/')
        else:
            flash("Invalid Credentials or more money is entered then account balance.", "warning")
    return render_template('take.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged Out of your Account', 'success')
    return redirect('/')

@app.route('/moneyLeft', methods=['POST', 'GET'])
def moneyLeft():
    if request.method=='POST':
        email = request.form.get("email")
        passwordAttempt = request.form.get("password")
        user =User.query.filter_by(email=email).first()
        password = user.password
        moneyleft  = user.money
        if passwordAttempt == password:
            return render_template("money.html", variable=moneyleft)
        else:
            flash("Invalid Password", "warning")
            return redirect("/")
    return render_template("money.html")

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/delete', methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        email = request.form.get("email")
        passwordAttempt = request.form.get("password")
        user =User.query.filter_by(email=email).first()
        password = user.password
        if passwordAttempt == password:
            db.session.delete(user)
            db.session.commit()
            flash("Account Deleted.", "secondary")
            return redirect("/")
        else:
            flash("Invalid Password", "danger")
            return redirect("/")
    return render_template("delete.html")

@app.route('/add_money', methods=['POST', 'GET'])
def AddMoney():
    if request.method=='POST':
        email = request.form.get("email")
        password = request.form.get("password")
        moneyAdded = request.form.get('value', type=int)
        print(moneyAdded)
        print(type(moneyAdded))
        user=User.query.filter_by(email=email).first()
        print(user.password)
        if user.password == password:
            user.money = user.money+moneyAdded
            db.session.commit()
            flash('Money Added to your account.', 'success')
            return redirect('/')
        else:
            flash("Invalid Credentials", "warning")
    return render_template('add.html')

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

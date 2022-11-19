from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from datetime import datetime
from flask import flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
# db.init_app(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost:7882/flask103"
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'the random string'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='flask103', template_mode='bootstrap4')


class Register(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    createdate = db.Column(db.Date, nullable=False)
    createtime = db.Column(db.Time, nullable=False)


admin.add_view(ModelView(Register, db.session))


@app.route("/", methods=['GET', 'POST'])
def Login():
    if "userid" in session:
        return redirect(url_for("Dashboard"))
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')
        # sql = Register.query.filter_by(name=name, password=password).all()
        sql = Register.query.filter_by(name=name, password=password)
        # print(len(sql))
        if sql.count() > 0:
            session['userid'] = sql.first().userid
            # return redirect("/dashboard")
            return redirect(url_for("Dashboard"))
    return render_template("index.html")


@app.route("/registration", methods=['GET', 'POST'])
def Registration():
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        createdate = date.today()
        now = datetime.now()
        createtime = now.strftime("%H:%M:%S")
        if password == cpassword:
            obj = Register(name=name, password=password,
                           createdate=createdate, createtime=createtime)
            db.session.add(obj)
            db.session.commit()
            flash("Registration Successful!")
    return render_template("registration.html")
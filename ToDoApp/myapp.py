from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.sqlite3'
app.config['SECRET_KEY'] = 'AS62nsfjadsaj_@dfjfsfhbf182sfjdfASFAKSF'


db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    Task_Date = db.Column(db.String)
    Task_Name = db.Column(db.String(100))
    Task_Email = db.Column(db.String(100), unique=True, nullable=True)
    Task_Phone = db.Column(db.String(100), unique=True, nullable=True)
    Task_Priority = db.Column(db.String(100))

    def __init__(self, tdate, tname, temail, tphone, tpri):
        self.Task_Date = tdate
        self.Task_Name = tname
        self.Task_Email = temail
        self.Task_Phone = tphone
        self.Task_Priority = tpri


@app.route('/')
def index():
    return render_template('index.html')


msg=None


@app.route('/add', methods=['GET', 'POST'])
def add():
    msg = None
    if request.method == 'POST':
        try:
            todo = Todo(
                request.form['t_date'], request.form['t_name'], request.form['t_email'], request.form['t_phone'], request.form['t_pri'])
            db.session.add(todo)
            db.session.commit()

            msg = "Task Added Successfully!"
            return render_template('index.html', msg=msg)
        except:
            msg = 'Email or Phone No Already Exists! Check Once!'
            return render_template('index.html', msg=msg)

    return render_template('index.html', msg=msg)


@app.route('/list')
def list():
    return render_template('list.html', todos=Todo.query.all())


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    todo = Todo.query.filter_by(id=id).first()

    if request.method == 'POST':
        try:
            todo.Task_Date = request.form['t_date']
            todo.Task_Name = request.form['t_name']
            todo.Task_Email = request.form['t_email']
            todo.Task_Phone = request.form['t_phone']
            todo.Task_Priority = request.form['t_pri']

            db.session.commit()
            msg = 'Task Updated!'
            return render_template('edit.html', msg=msg, todo=todo)
        except:
            msg = 'Task Updation Failed!'
            return render_template('edit.html', msg=msg, todo=todo)
    else:
        return render_template('edit.html', todo=todo)


@app.route('/delete/<id>')
def delete(id):
    try:
        Todo.query.filter_by(id=id).delete()
        db.session.commit()
        msg = 'Task Deleted SuccessFully'
        return render_template('list.html', msg=msg, todos=Todo.query.all())
    except:
        flash('Unable to delete!')

    return redirect(url_for('index'))



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


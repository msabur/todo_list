from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash
from . import app, db
from .forms import LoginForm, TaskForm, RegisterForm
from .models import User, Task
from flask import render_template, flash, request, url_for, redirect
from flask_login import login_user, current_user, logout_user, login_required
from .site_nav import navbar


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    name = current_user.username
    tasks = Task.query.filter_by(author=current_user)
    form = TaskForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        status = form.status.data
        newTask = Task(
            title=title, description=description, status=status, author=current_user
        )
        db.session.add(newTask)
        db.session.commit()

    return render_template("index.html", name=name, tasks=tasks, form=form)


@app.route("/deleteTask/<id>", methods=["GET"])
def deleteTask(id):
    toDelete = Task.query.get(id)

    if toDelete == None or toDelete.author != current_user:
        flash(f"You don't have a task with id {id}", "error")
        return redirect(url_for("index"))

    db.session.delete(toDelete)
    db.session.commit()
    flash("Deleted successfully!", "success")
    return redirect(url_for("index"))


@app.route("/editTask/<id>", methods=["GET", "POST"])
def editTask(id):
    toEdit = Task.query.get(id)

    if toEdit == None or toEdit.author != current_user:
        flash(f"You don't have a task with id {id}", "error")
        return redirect(url_for("index"))

    form = TaskForm(
        data={
            "title": toEdit.title,
            "description": toEdit.description,
            "status": toEdit.status,
        }
    )

    if form.validate_on_submit():
        toEdit.title = form.title.data
        toEdit.description = form.description.data
        toEdit.status = form.status.data
        db.session.commit()
        flash("Updated successfully!", "success")

    return render_template("editTask.html", task=toEdit, form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password.", "warning")
            return redirect(url_for("login"))

        login_user(user)
        flash("Logged in successfully.", "success")

        next = request.args.get("next")
        if not next or url_parse(next).netloc != "":
            return redirect(url_for("index"))

        return redirect(next)
    return render_template("login.html", form=form, title="Login")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash(
                f"Username {form.username.data} is taken. Please choose a different username.",
                "warning",
            )
            return redirect(url_for("register"))

        hash = generate_password_hash(form.password.data)
        newUser = User(username=form.username.data, password_hash=hash)
        db.session.add(newUser)
        db.session.commit()

        flash("Registered successfully.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/profile")
def profile():
    return render_template("under_construction.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.show import Show
from flask_app.models.user import User




# -----------------------------------------------------------------------------

@app.route('/new/show')
def new_show():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('new_show.html',user=User.get_by_id(session['user_id']))

@app.route('/create/show',methods=['POST'])
def create_show():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Show.validate_show(request.form):
        return redirect('/new/show')
    data = {
        "title": request.form["title"],
        "network": request.form["network"],
        "release_date": request.form["release_date"],
        "description": request.form["description"],
        "user_id": session["user_id"]
    }
    Show.save(data)
    return redirect('/dashboard')

@app.route('/edit/show/<int:id>')
def edit_show(id):
    data = {
        "id":id
    }
    if 'user_id' not in session:
        return redirect('/logout')
    show = Show.get_one(data)
    if session['user_id'] != show.user_id:
        return redirect('/logout')
    return render_template("edit_show.html",edit=Show.get_one(data),user=User.get_by_id(session['user_id']))

@app.route('/update/show',methods=['POST'])
def update_show():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Show.validate_show(request.form):
        return redirect(f'/edit/show/{request.form["id"]}')
    data = {
        "title": request.form["title"],
        "network": request.form["network"],
        "release_date": request.form["release_date"],
        "description": request.form["description"],
        "id": request.form['id']
    }
    Show.update(data)
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def show_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    return render_template("show_show.html",show=Show.get_one(data),user=User.get_by_id(session['user_id']),count_likes=Show.count_likes(data))

@app.route('/destroy/show/<int:id>')
def destroy_show(id):
    data = {
        "id": id
    }
    if 'user_id' not in session:
        return redirect('/logout')
    show = Show.get_one(data)
    if session['user_id'] != show.user_id:
        return redirect('/logout')
    Show.destroy(data)
    return redirect('/dashboard')

# --------------------------BASIC CRUD ABOVE ------------------------------

@app.route('/like/show/<int:id>')
def like_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user_id": session["user_id"],
        "id" : id
    }
    Show.like_show(data)
    return redirect('/dashboard')

@app.route('/unlike/show/<int:id>')
def unlike_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "user_id": session["user_id"],
        "id" : id
    }
    Show.unlike_show(data)
    return redirect('/dashboard')

# since the user is in session there is no harm in them being able to manually
# type into their url /like/show/<int:id> or /unlike/show/<int:id>
# as they have permission to do this on any tv show
# unlike editing or deleting other tv shows that they didn't create
# which we protected.
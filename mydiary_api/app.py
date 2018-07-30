"""
api endpoints are defined in this file
"""

from flask import Flask, render_template, request, \
    jsonify, abort, make_response, request, url_for, \
    flash, redirect
from flask_restful import Resource, Api
from functools import wraps
import datetime
import jwt

from mydiary_api.mydiary import DiaryEntry, Entries, User, MyDiary
from db_mydiary.db import MyDiary_Database
from mydiary_api.v1 import GetEntry



app = Flask(__name__)
#api = Api(app)
NOW = datetime.datetime.now()

app.config['SECRET_KEY'] = 'secret'

my_diary_object = MyDiary()
app_db = MyDiary_Database()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message' : 'You need to login first!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'You are unauthorized to acces this data!'}), 401
        return f(*args, **kwargs)
    return wrap

""" links to the login page """
@app.route('/login', methods=['GET', 'POST'])
def login(email):
    if request.method == 'POST':
        if not request.json or not 'email' in request.json or not 'password' in request.json:
            abort(400)
        else:
            email=request.json.get('email', "")
            password=request.json.get('password', "")
            logged_in = my_diary_object.current_user.login(email, password)
            if logged_in == "You've been logged in successfully":
                token = jwt.encode({'user' : user_id , 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
                return jsonify({'login' : 'sucessful', 'token' : token.decode('UTF-8') })
            else:
                return jsonify({'login' : logged_in})
 

""" this route links to the login page """
@app.route('/registration', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if not request.json or not 'email' in request.json or not 'name' in request.json or not 'password' in request.json:
            message = "unable to add user"
            abort(400)
        else:
            name_data=request.json.get('name', "")
            email_data=request.json.get('email', "")
            password_data=request.json.get('password', "")
            user = {
            user_id : None,
            user_name : name_data,
            user_email : email_data,
            user_password : password_data
            }
            my_diary_object.addUser(user)
            message = "added successfully"
            return jsonify({'new_user' : user})
        return message


""" returns a single diary entry """
@app.route('/home/api/v1/entries/<int:diary_entry_id>', methods=['GET'])
#@login_required
def get_entry(diary_entry_id):
    """ outputs one user entry """
    #token = request.args.get('token')
    #data = jwt.decode(token, app.config['SECRET_KEY'])

    entry = my_diary_object.user_entries.getOneEntry(user_id, diary_entry_id)
    if entry == None:
        return jsonify({'error': 'Bad request, the specified entry does not exist.'})
    else:
        return jsonify({'entry':entry})


""" returns all diary entries """
@app.route('/home/api/v1/entries', methods=['GET'])
#@login_required
def get_all_entries():
    """ this method outputs all entries """
    #token = request.args.get('token')
    #data = jwt.decode(token, app.config['SECRET_KEY'])

    entry_list = my_diary_object.user_entries.getAllEntries(user_id)
    if len(entry_list) == 0:
        abort(404)
    else:
        return jsonify([{'entrylist':entry_list[:]}])


""" this route adds single diary entry """
@app.route('/home/api/v1/entries', methods=['POST'])
#@login_required
def post_entry():
    """ this method creates a new entry """
    #token = request.args.get('token')
    #data = jwt.decode(token, app.config['SECRET_KEY'])

    exists = False
    if not request.json or not 'entrydata' in request.json:
        abort(400)
    else:
        entry_data=request.json.get('entrydata', "")
        title_data=request.json.get('entrytitle', "")
        current_time="".join(str(NOW.day)+"/"+str(NOW.month)\
                +"/"+str(NOW.year))
        entry_id_data = None #int(my_diary_object.user_entries.entry_index) + 1
        my_diary_object.user_entries.addEntry(entry_id, user_id, title_data, entry_data, current_time)
        
        rows = app_db.cursor.fetchall()
        for row in rows:
            if (entrydata == row[3]):
                # AND (title == row[2]):
                exists = True
        if exists:
            return jsonify(['error!':'this entry already exists.'])
        else:
            entry = {
                'entry_id' : entry_id,
                'user_id' : user_id,
                'title' : title
                'entrydata' : entrydata,
                'datecreated' : current_time
            }
    return jsonify({'entry added': entry})


""" this route updates a single diary entry """
@app.route('/home/api/v1/entries/<int:diary_entry_id>', \
                methods=['PUT'])
#@login_required
def put_entry(user_id, diary_entry_id):
    """ this method updates an entry's data """
    #token = request.args.get('token')
    #data = jwt.decode(token, app.config['SECRET_KEY'])

    app_db.cursor.execute("SELECT * from entries WHERE user_id = %s AND entry_id = %s")
    rows = app_db.cursor.fetchall()
    if rows == []:
        abort(404)
    elif not request.json:
        abort(400)
    elif 'entrydata' in request.json and \
                type(request.json['entrydata']) is not unicode:
        abort(400)
    elif 'title' in request.json and type(request.json['title']) is not str:
        abort(400)
    entry_data = request.json.get('entrydata', "")
    title_data = request.json.get('entrytitle', "")
    current_time="".join(str(NOW.day)+"/"+str(NOW.month)\
                 +"/"+str(NOW.year)))
    entry_id_data = diary_entry_id
    my_diary_object.user_entries.modifyEntry(title, entrydata, current_time, entry_id_data)
    entry = {
        'entry_id': diary_entry_id,
        'user_id': user_id,
        'title':title
        'entrydata':entrydata,
        'datecreated':current_time
    }
    return jsonify({'entry':entry})

""" this route deletes a diary entry """
@app.route('/home/api/v1/entries/<int:diary_entry_id>', methods=['DELETE'])
#@login_required
def delete_entry(diary_entry_id):
    """ this method deletes an entry """
    #token = request.args.get('token')
    #data = jwt.decode(token, app.config['SECRET_KEY'])

    app_db.cursor.execute("SELECT * from entries WHERE user_id = %s AND entry_id = %s")
    rows = app_db.cursor.fetchall()
    if rows == []:
        abort(404)
    my_diary_object.user_entries.deleteEntry(entry_id)
    return jsonify({'result':True})

@app.errorhandler(404)
def not_found(error):
    """ error handler gives more friendly errors """
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    """ error handler gives more friendly errors """
    return make_response(jsonify({'error': 'Bad request, \
                please review your input data'}), 400)

def main(self):
    app_db.cursor.execute("""INSERT INTO users (user_id, name, email, password) VALUES (1, 'Gordon Balaaka', 'balaakagordon@gmail.com', 'password');""")
    app_db.cursor.execute("""INSERT INTO users (user_id, name, email, password) VALUES (2, 'James Bond', '007.amesbond@gmail.com', 'bondjamesbond');""")
    app_db.cursor.execute("""INSERT INTO entries (entry_id, user_id, title, data, date) VALUES (1, 1, 'My first entry', 'Today, I learned to use postgres databases', '28/07/18');""")
    app_db.cursor.execute("""INSERT INTO entries (entry_id, user_id, title, data, date) VALUES (1, 1, 'My first entry', 'Today, I integrated my database with my project', '29/07/18');""")
    #gordonbalaaka = User("Gordon Balaaka", \
                    #"balaakagordon@gmail.com", \
                    #"password", my_diary_object)
    #seconduser = User("Peter Crouch", \
                    #"petercrouch@gmail.com", "password", my_diary_object)
    #jamesbond = User("James Bond", "007.amesbond@gmail.com", \
                    #"bondjamesbond", my_diary_object)
    #my_diary_object.login("balaakagordon@gmail.com", "password")
    #entry1 = DiaryEntry(entry_list=my_diary_object.user_entries, \
                    #data='this is my first entry', \
                    #current_time="".join(str(NOW.day)+"/"\
                    #+str(NOW.month)+"/"+str(NOW.year)))
    #entry2 = DiaryEntry(entry_list=my_diary_object.user_entries, \
                    #data='this is my second entry', \
                    #current_time="".join(str(NOW.day)+"/"\
                    #+str(NOW.month)+"/"+str(NOW.year)))


if __name__ == '__main__':
    app.run(debug=True)

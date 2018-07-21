"""
api endpoints are defined in this file
"""

from flask import Flask, render_template, request, \
    jsonify, abort, make_response, request, url_for, \
    flash, redirect
from flask_restful import Resource, Api
import datetime
import mydiary
from mydiary import DiaryEntry



#app = Flask(__name__)
app = Flask(__name__)
api = Api(app)
NOW = datetime.datetime.now()


""" this route links to the welcome page """
@app.route('/')
def welcome():
    return render_template('index.html')

""" this route links to the home page """
@app.route('/home')
def home():
    return render_template('index.html')

""" this route links to the login page """
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != 'admin') \
                or request.form['password'] != 'admin':
            error = "Invalid Credentials"
        else:
            flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

""" this route logs the user out """
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))


""" this route returns a single diary entry """
@app.route('/home/api/v1/entries/<int:entry_id>', methods=['GET'])
def get_entry(entry_id):
    """ this method outputs one entry """

    entry = [entry for entry in mydiaryobject.userEntries.entrylist if entry.entryId == entry_id]
    entry = {'id': entry[0].entryId, 'entrydata': entry[0].data, 'datecreated': entry[0].created}
    if entry == []: #or entry[0].entryId == None:
        abort(404)
    return jsonify({'entry': entry})

""" this route returns all diary entries """
@app.route('/home/api/v1/entries', methods=['GET'])
def get_all_entries():
    """ this method outputs all entries """

    if len(mydiaryobject.userEntries.entrylist) == 0:
        abort(404)

    entrylist = []
    for entry in mydiaryobject.userEntries.entrylist:
        entry = {'id': entry.entryId, 'entrydata': entry.data, 'datecreated': entry.created}
        entrylist.append(entry)
    return jsonify([{'entrylist': entrylist[:]}])

""" this route adds single diary entry """
@app.route('/home/api/v1/entries', methods=['POST'])
def create_entry():
    """ this method creates a new entry """

    if not request.json or not 'entrydata' in request.json:
        abort(400)
    entry = mydiaryobject.userEntries.createEntry
    new_entry = DiaryEntry(entryList=mydiaryobject.userEntries, \
    data=request.json.get('entrydata', ""), currentTime="".join(str(NOW.day)\
    +"/"+str(NOW.month)+"/"+str(NOW.year)))
    entry = {
        'id': new_entry.entryId,
        'entrydata': new_entry.data,
        'datecreated': new_entry.created
    }
    return jsonify({'entry': entry})

""" this route updates a single diary entry """
@app.route('/home/api/v1/entries/<int:entry_id>', methods=['PUT'])
def update_task(entry_id):
    """ this method updates an entry's data """

    entry = [entry for entry in mydiaryobject.userEntries.entrylist if entry.entryId == entry_id]
    if len(entry) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'date' in request.json and type(request.json['date']) is not int:
        abort(400)
    entry[0].data = request.json.get('entrydata', "")
    entry = {'id': entry[0].entryId, 'entrydata': entry[0].data, 'datecreated': entry[0].created}
    return jsonify({'entry': entry})

""" this route deletes a diary entry """
@app.route('/home/api/v1/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """ this method deletes an entry """

    entry_list = [entry for entry in mydiaryobject.userEntries.entrylist \
    if entry.entryId == entry_id]
    if entry_list == []:
        abort(404)
    mydiaryobject.userEntries.entrylist.remove(entry_list[0])
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    """ error handler gives more friendly errors """
    return make_response(jsonify({'error': 'Not found'}), 404)

mydiaryobject = mydiary.MyDiary()
gordonbalaaka = mydiary.User("Gordon Balaaka", "balaakagordon@gmail.com", "password", mydiaryobject)
seconduser = mydiary.User("Peter Crouch", "petercrouch@gmail.com", "password", mydiaryobject)
jamesbond = mydiary.User("James Bond", "007.amesbond@gmail.com", "bondjamesbond", mydiaryobject)
mydiaryobject.login("balaakagordon@gmail.com", "password")
entry1 = DiaryEntry(entryList=mydiaryobject.userEntries, \
        data='this is my first entry', currentTime="".join(str(NOW.day)\
        +"/"+str(NOW.month)+"/"+str(NOW.year)))
entry2 = DiaryEntry(entryList=mydiaryobject.userEntries, \
        data='this is my second entry', currentTime="".join(str(NOW.day)\
        +"/"+str(NOW.month)+"/"+str(NOW.year)))


if __name__ == '__main__':
    app.run(debug=True)

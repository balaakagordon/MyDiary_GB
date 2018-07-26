"""
api endpoints are defined in this file
"""

from flask import Flask, render_template, request, \
    jsonify, abort, make_response, request, url_for, \
    flash, redirect
from flask_restful import Resource, Api
import datetime
import mydiaryapp.mydiary
from mydiaryapp.mydiary import DiaryEntry


app = Flask(__name__)
api = Api(app)
NOW = datetime.datetime.now()

""" this route returns a single diary entry """
@app.route('/home/api/v1/entries/<int:diary_entry_id>', methods=['GET'])
def get_entry(diary_entry_id):
    """ this method outputs one entry """
    diary_entry_list = [entry for entry in \
                my_diary_object.user_entries.entry_list if \
                entry.entry_id == diary_entry_id]
    if diary_entry_list == []:
        return jsonify({'error': 'Bad request, that ID does not exist.'})
    else:
        entry = {'id':diary_entry_list[0].entry_id, \
            'entrydata':diary_entry_list[0].data, \
            'datecreated':diary_entry_list[0].created}
    return jsonify({'entry':entry})

""" this route returns all diary entries """
@app.route('/home/api/v1/entries', methods=['GET'])
def get_all_entries():
    """ this method outputs all entries """
    if len(my_diary_object.user_entries.entry_list) == 0:
        abort(404)
    diary_entry_list = []
    for entry in my_diary_object.user_entries.entry_list:
        entry = {
            'id':entry.entry_id, 
            'entrydata':entry.data, 
            'datecreated':entry.created
        }
        diary_entry_list.append(entry)
    return jsonify([{'entrylist':diary_entry_list[:]}])

""" this route adds single diary entry """
@app.route('/home/api/v1/entries', methods=['POST'])
def create_entry():
    """ this method creates a new entry """
    #if not request.json or not 'entrydata' in request.json:
        #abort(400)
    entry = my_diary_object.user_entries.createEntry
    entry_list = [entry for entry in \
                my_diary_object.user_entries.entry_list]
    new_entry = DiaryEntry(entry_list=my_diary_object.user_entries, \
                data=request.json.get('entrydata', ""), \
                current_time="".join(str(NOW.day)+"/"+str(NOW.month)\
                +"/"+str(NOW.year)))
    for i in range(len(entry_list)):
        if new_entry.data == entry_list[i].data:
            return jsonify({'error!': "this entry already exists"})
        else:
            entry = {
                'id': new_entry.entry_id,
                'entrydata':new_entry.data,
                'datecreated':new_entry.created
            }
    return jsonify({'entry': entry})

""" this route updates a single diary entry """
@app.route('/home/api/v1/entries/<int:diary_entry_id>', \
                methods=['PUT'])
def update_task(diary_entry_id):
    """ this method updates an entry's data """
    diary_entry_list = [entry for entry in \
                my_diary_object.user_entries.entry_list if \
                entry.entry_id == diary_entry_id]
    if len(diary_entry_list) == 0:
        abort(404)
    if not request.json:
        abort(400)
    #if 'entrydata' in request.json and \
                #type(request.json['entrydata']) is not unicode:
        abort(400)
    if 'date' in request.json and type(request.json['date']) is not str:
        abort(400)
    diary_entry_list[0].data = request.json.get('entrydata', "")
    entry = {'id': diary_entry_list[0].entry_id, \
                'entrydata':diary_entry_list[0].data, \
                'datecreated':diary_entry_list[0].created}
    return jsonify({'entry':entry})

""" this route deletes a diary entry """
@app.route('/home/api/v1/entries/<int:diary_entry_id>', methods=['DELETE'])
def delete_entry(diary_entry_id):
    """ this method deletes an entry """
    diary_entry_list = [entry for entry in \
                my_diary_object.user_entries.entry_list if \
                entry.entry_id == diary_entry_id]
    if diary_entry_list == []:
        abort(404)
    my_diary_object.user_entries.entry_list.remove(diary_entry_list[0])
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

my_diary_object = mydiaryapp.mydiary.MyDiary()
gordonbalaaka = mydiaryapp.mydiary.User("Gordon Balaaka", \
                "balaakagordon@gmail.com", \
                "password", my_diary_object)
seconduser = mydiaryapp.mydiary.User("Peter Crouch", \
                "petercrouch@gmail.com", "password", my_diary_object)
jamesbond = mydiaryapp.mydiary.User("James Bond", "007.amesbond@gmail.com", \
                "bondjamesbond", my_diary_object)
my_diary_object.login("balaakagordon@gmail.com", "password")
entry1 = DiaryEntry(entry_list=my_diary_object.user_entries, \
                data='this is my first entry', \
                current_time="".join(str(NOW.day)+"/"\
                +str(NOW.month)+"/"+str(NOW.year)))
entry2 = DiaryEntry(entry_list=my_diary_object.user_entries, \
                data='this is my second entry', \
                current_time="".join(str(NOW.day)+"/"\
                +str(NOW.month)+"/"+str(NOW.year)))


if __name__ == '__main__':
    app.run(debug=True)

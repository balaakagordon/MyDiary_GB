from flask import Flask, request, jsonify, abort, make_response
from flask_restful import Resource, Api
import datetime


app = Flask(__name__)
api = Api(app)
now = datetime.datetime.now()
##app.config['SECRET_KEY'] = "my precious"


entries = [
    {
        'id': 1,
        'entrydata': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'datecreted': "".join(str(now.day)+"/"+str(now.month)\
                        +"/"+str(now.year))
    },
    {
        'id': 2,
        'entrydata': u'Need to find a good Python tutorial on the web', 
        'datecreated': "".join(str(now.day)+"/"+str(now.month)\
                        +"/"+str(now.year))
    }
]


@app.route('/home/api/v1/entries/<int:entry_id>', methods=['GET'])
def get_entry(entry_id):
    entry = [entry for entry in entries if entry['id'] == entry_id]
    if len(entry) == 0:
        abort(404)
    return jsonify({'entry': entry[0]})

@app.route('/home/api/v1/entries', methods=['GET'])
def get_all_entries():
    entrylist = [entry for entry in entries]
    if len(entry) == 0:
        abort(404)
    return jsonify([{'entrylist': entrylist[:]}])

@app.route('/home/api/v1/entries', methods=['POST'])
def create_entry():
    if not request.json or not 'entrydata' in request.json:
        abort(400)
    entry = {
        'id': entries[-1]['id'] + 1,
        'entrydata': request.json.get('entrydata', ""),
        'datecreated': "".join(str(now.day)+"/"+str(now.month)\
                        +"/"+str(now.year))
    }
    entries.append(entry)
    return jsonify({'entry': entry})

@app.route('/home/api/v1/entries/<int:entry_id>', methods=['PUT'])
def update_task(entry_id):
    entry = [entry for entry in entries if entry['id'] == entry_id]
    if len(entry) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'date' in request.json and type(request.json['date']) is not int:
        abort(400)
    entry[0]['entrydata'] = request.json.get('entrydata', entry[0]['entrydata'])
    entry[0]['datecreated'] = request.json.get('datecreated', entry[0]['datecreated'])
    return jsonify({'entry': entry[0]})

@app.route('/home/api/v1/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    entry = [entry for entry in entries if entry['id'] == entry_id]
    if len(entry) == 0:
        abort(404)
    entries.remove(entry[0])
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
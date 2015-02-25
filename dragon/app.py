#!flask/bin/python

import sys
import json

#sys.path.append('/Library/Python/2.7/site-packages')

from flask import Flask, jsonify, render_template, request
from db_client import MongoDB


app = Flask(__name__, static_url_path='/static')

fail_response = {
    'status': 420,
    'updated': u'None',
    'description': u'Error updating'}

# public pages
@app.route('/')
def homepage():
    return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html')


# special api that checks if char exists in DB
@app.route('/mw/api/v1/user', methods=['POST'])
def get_user():
    mongo = MongoDB()
    mana_db = mongo.get_manaworld_database()

    data = json.loads(request.data)

    try:
        # searcing for character in database
        result = mana_db.ManaWorldDB.find({"charachters.char_name": data["character"]}, {"char_name": 1})
        if not result == None:
            return jsonify({'status': '200', 'description': 'true'})
        else:
            return jsonify({'status': '400', 'description': 'false'})

    except:
        return jsonify({'status': '400', 'description': data["character"]})


# api routes
@app.route('/mw/api/v1/battle', methods=['POST'])
def get_battles():
    mongo = MongoDB()
    mana_db = mongo.get_manaworld_database()

    data = json.loads(request.data)

    try:
        # updating battles for charachter database
        char = data["character"]

        query = mana_db.ManaWorldDB.update(
            {"charachters.char_name": char},
            {"$push": {"charachters.$.battle_chat": data["battle"]}})

        return jsonify({'status': '200', 'updated': 'battle', 'updated_charachter': data["character"]})

    except:
        return jsonify(fail_response)


@app.route('/mw/api/v1/debug', methods=['POST'])
def get_debug():
    mongo = MongoDB()
    mana_db = mongo.get_manaworld_database()

    data = json.loads(request.data)

    try:
        # updating debug log for charachter database
        char = data["character"]["character"]

        query = mana_db.ManaWorldDB.update({"charachters.char_name": char},
                                           {"$push": {"charachters.$.debug_chat": data["debug"]}})

        return jsonify({'status': '200',
                        'updated': 'debug',
                        'updated_charachter': char})
    except:
        return jsonify(fail_response)


@app.route('/mw/api/v1/general', methods=['POST'])
def get_general():
    mongo = MongoDB()
    mana_db = mongo.get_manaworld_database()

    data = json.loads(request.data)

    char = data["character"]["character"]

    try:
        # updating debug log for charachter database

        query = mana_db.ManaWorldDB.update({"charachters.char_name": char},
                                           {"$push": {"charachters.$.general_chat": data["general"]}})

        return jsonify({'status': '200',
                        'updated': 'general',
                        'updated_charachter': char})
    except:
        return jsonify(fail_response)


@app.route('/mw/api/v1/party', methods=['POST'])
def get_party():
    mongo = MongoDB()
    mana_db = mongo.get_manaworld_database()

    data = json.loads(request.data)

    try:
        # updating parties for charachter database
        char = data["character"]["character"]

        query = mana_db.ManaWorldDB.update(
            {"charachters.char_name": char},
            {"$push": {"charachters.$.party_chat": data["parties"]}})

        return jsonify({'status': '200',
                        'updated': 'party',
                        'updated_charachter': char})
    except:
        return jsonify(fail_response)


@app.route('/mw/api/v1/trade', methods=['POST'])
def get_trade():
    mongo = MongoDB()
    mana_db = mongo.get_manaworld_database()

    data = json.loads(request.data)

    try:
        # updating parties for character database
        char = data["character"]["character"]

        query = mana_db.ManaWorldDB.update(
            {"charachters.char_name": char},
            {"$push": {"charachters.$.trade_chat": data["trades"]}})

        return jsonify({'status': query,
                        'updated': data["trades"],
                        'updated_character': char})
    except:
        return jsonify(fail_response)


@app.route('/mw/api/v1/whisper', methods=['POST'])
def get_whisper():
    mongo = MongoDB()
    mana_db = mongo.get_manaworld_database()

    data = json.loads(request.data)
    char = data["character"]["character"]

    try:
        # updating whispers for charachter database
        mana_db.ManaWorldDB.update(
            {"charachters.char_name": char},
            {"$push": {"charachters.$.whisper_chat": data["whispers"]}})

        return jsonify({'status': '200',
                        'updated': 'whispers',
                        'updated_charachter': data["character"]})
    except:
        return jsonify(fail_response)


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host="178.62.125.198")
from flask import Flask, request, jsonify, g
from datetime import datetime
import json

from Database import get_db, close_db, exec, fetch, init_db

app = Flask(__name__)

@app.teardown_appcontext
def close_database(exception):
    close_db(exception)

def calculateAgeInDays(birth_date):
    birth_date_obj = datetime.strptime(birth_date, '%d-%m-%Y')
    today = datetime.now()
    ageInDays = (today - birth_date_obj).days
    age = f"{ageInDays} days"
    return age

@app.route('/age', methods=['GET'])
def getAge():
    with open("BirthDate.json", "r") as f:
        data = json.load(f)
        birth_date = data.get("birth_date")
    age = calculateAgeInDays(birth_date)

    output = {
        "age": f"{age}"
    }

    with open("age.json", "w") as file:
        json.dump(output, file)

    return jsonify(output)

@app.route("/FullName", methods=["POST", "GET"])
def postFullName():
    with open("age.json", "r") as f:
        info = json.load(f)
        full_name = info.get("Full Name")
        age = info.get("age")

        if full_name and age:
            exec("INSERT INTO Credentials (FullName, age) VALUES (?,?)",(full_name, age))
            return jsonify(info)
        else:
            return jsonify({"ERROR": "Full Name not found in json file"})

@app.route("/view", methods=["GET"])
def view():
    entries = fetch("SELECT FullName, age FROM Credentials")
    print(entries)
    return jsonify(entries)

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
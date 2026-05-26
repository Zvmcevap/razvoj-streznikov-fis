import json
from flask import Flask, redirect, url_for, request, render_template, session, jsonify

app = Flask(__name__)
app.secret_key = "zamenjaj_me_z_dolgim_nakljucnim_nizom"

us_pass = {
    "martin": "martin00",
    "student": "student00"
}

@app.route("/success/<name>")
def success(name):
    if "username" not in session or session["username"] != name:
        return redirect(url_for("login"))
    return f"Welcome, {name}"

@app.route("/failure")
def failure():
    return "Wrong username or password"

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    user = request.form.get("username")
    password = request.form.get("password")

    if user in us_pass and us_pass[user] == password:
        session["username"] = user
        return redirect(url_for("success", name=user))

    return redirect(url_for("failure"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))



@app.route('/getall', methods=['GET'])
def queryall():
    with open('data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        return jsonify(records)
#        return jsonify({'error': 'data not found'})

@app.route('/', methods=['POST'])
def create():
    record = json.loads(request.data)
    with open('data.txt', 'r') as f:
        data = f.read()
    if not data:
        records = [record]
    else:
        records = json.loads(data)
        records.append(record)
    with open('data.txt', 'w') as f:
        f.write(json.dumps(records, indent=2))
    return jsonify(record)

@app.route('/', methods=['PUT'])
def update():
    record = json.loads(request.data)
    new_records = []
    with open('data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
    for r in records:
        if r['ime'] == record['ime']:
            r['visina'] = record['visina']
        new_records.append(r)
        
    print(new_records)
    with open('data.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify(record)
    
@app.route('/', methods=['DELETE'])
def delete():
    record = json.loads(request.data)
    new_records = []
    with open('data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for r in records:
            if r['ime'] == record['ime']:
                continue
            new_records.append(r)
    with open('data.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify(record)


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True, port=1235, use_reloader=False)
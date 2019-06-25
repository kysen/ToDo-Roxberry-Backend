from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow

from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://xadovgalssfyws:30e847ec6f5af082037f420f149d9e5ddf120d568955cb8bbc3b7fe17841c783@ec2-54-235-104-136.compute-1.amazonaws.com:5432/d919s2qgv5ccs6"

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class SaveByDate (db.Model):
    __tablename__="SaveListDaily"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.String(3), nullable=True)
    category = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)

    def __init__(self, title, done, category, date):
        self.title = title
        self.done = done
        self.category = category
        self.date = date

class DateSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "done", "category", "date")

date_schema = DateSchema()
dates_schema = DateSchema(many=True)

@app.route("/dates", methods=["GET"])
def get_dates():
    all_dates = Date.query.all()
    result = dates_schema.dump(all_dates)
    return jsonify(result.data)

@app.route("/date-add", methods=["POST"])
def add_date():

    title = request.json["title"]
    done = request.json["done"]
    category = request.json["category"]
    date = request.json["date"]

    record = Date(title, done, category, date)

    db.session.add(record)
    db.session.commit()

    date = Date.query.get(record.id)

    return date_schema.jsonify(date)

# @app.route("/date/<id>", methods=["DELETE"])
# def delete_date(id):
#     record = Date.query.get(id)
#     db.session.delete(record)
#     db.session.commit()


class Todo (db.Model):
    __tablename__="todoLists"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.String(3), nullable=True)
    category = db.Column(db.String(100), nullable=False)

    def __init__(self, title, done, category):
        self.title = title
        self.done = done
        self.category = category

class TodoSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "done", "category")

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)


@app.route("/todo-add", methods=["POST"])
def add_todo():

    title = request.json["title"]
    done = request.json["done"]
    category = request.json["category"]

    record = Todo(title, done, category)

    db.session.add(record)
    db.session.commit()

    todo = Todo.query.get(record.id)

    return todo_schema.jsonify(todo)


@app.route("/todos", methods=["GET"])
def get_todos():
    all_todos = Todo.query.all()
    result = todos_schema.dump(all_todos)
    return jsonify(result.data)

@app.route("/todo/<id>", methods=["PATCH"])
def update_todo(id):

    todo = Todo.query.get(id)

    new_done = request.json["done"]

    todo.done = new_done

    db.session.commit()
    return todo_schema.jsonify(todo)


@app.route("/todo/<id>", methods=["DELETE"])
def delete_todo(id):
    record = Todo.query.get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify("RECORD DELETED!")

if __name__ == "__main__":
    app.debug = True
    app.run()
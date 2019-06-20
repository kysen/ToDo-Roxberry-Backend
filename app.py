from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow

from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://usrqsnkdojrrwi:a30bb487978f0e03d3059a81160fe79e871f99378638cdcaa0900baa795034c1@ec2-174-129-27-3.compute-1.amazonaws.com:5432/dd40et8qqjcla1"

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Todo (db.Model):
    __tablename__="todoLists"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean)
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
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()   

class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.Text)
    due_by = db.Column(db.Integer)
    Not_Started = db.Column(db.Integer,default=0)
    In_Progress = db.Column(db.Integer,default=0)
    Finished = db.Column(db.Integer,default=0)

    def __init__(self,task,due_by,Not_Started,In_Progress,Finished):
        self.task = task
        self.due_by = due_by
        self.Not_Started = Not_Started
        self.In_Progress = In_Progress
        self.Finished = Finished

    def __repr__(self):
        return f"Task {self.task} is due by {self.due_by}."
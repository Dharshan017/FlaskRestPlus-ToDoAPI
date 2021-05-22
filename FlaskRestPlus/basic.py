from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from myproject.models import Todo
from myproject import db,app

# app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app,title='TODO_API')
ns = api.namespace('TODO\'s', description='TODO operations')

todoState = api.model('TodoState',{
    'Not_Started': fields.Integer(description='Work is Not Started Yet!'),
    'In_Progress': fields.Integer(description='Work is Started But Not Finished Yet!'),
    'Finished': fields.Integer(description='Work is Finished!'),
})

todo = api.model('Todo', {
    'task': fields.String(required=True, description='Task Details'),
    'due_by':fields.Date(required=True,description='Deadline For Task to be Finished!'),
    'status':fields.Nested(todoState),
})

todoUpdate = api.model('TodoUpdate', {
    'task': fields.String(readonly=True, description='Task Details'),
    'due_by':fields.Date(readonly=True,description='Deadline For Task to be Finished!'),
    'status':fields.Nested(todoState),
})

@ns.route("/")
class TodoList(Resource):
    @ns.doc("List Of Todos")
    @ns.marshal_list_with(todo,code=201)
    def get(self):
        '''List Of All Tasks..'''   
        Obj = Todo.query.all()
        res = []
        for i in Obj:
            res.append({
                "id":i.id,
                "task":i.task,
                "due_by":i.due_by,
                "status":{
                    "Not_Started":i.Not_Started,
                    "In_Progress":i.In_Progress,
                    "Finished":i.Finished,
                },
            })
        return res,201
    
    @ns.doc("Create a Todo")
    @ns.expect(todo)
    @ns.marshal_with(todo,code=201)
    def post(self):
        '''Create a New Tasks...'''
        data = api.payload
        obj = Todo(
            data['task'],
            data['due_by'],
            data['status']['Not_Started'],
            data['status']['In_Progress'],
            data['status']['Finished'],
        )
        db.session.add(obj)
        db.session.commit()
        return api.payload,201  

@ns.param("id","Unique Identifier for Tasks")
@ns.response(404,"Requested ID Not Found!")
@ns.route("/<int:id>")
class TodoR(Resource):
    @ns.doc("A Todo")
    @ns.marshal_with(todo,code=201)
    def get(self,id):
        '''Fetch the Task for Given Id..'''
        Obj = Todo.query.get(id)
        res = {
                "id":Obj.id,
                "task":Obj.task,
                "due_by":Obj.due_by,
                "status":{
                    "Not_Started":Obj.Not_Started,
                    "In_Progress":Obj.In_Progress,
                    "Finished":Obj.Finished,
                },
            }
        return res,201
    
    @ns.doc("Delete a Todo")
    @ns.marshal_with(todo,code=201)
    def delete(self,id):
        '''Delete the Task with Given Id...'''
        db.session.delete(Todo.query.get(id))
        db.session.commit()
        return '',201
    
    @ns.expect(todoUpdate)
    @ns.marshal_with(todoUpdate,code=201)
    @ns.doc("Update a Todo")
    def put(self,id):
        '''Update The Status of Todo For a Given Id'''
        obj = Todo.query.get(id)
        data = api.payload
        obj.Not_Started = data['status']['Not_Started']
        obj.In_Progress = data['status']['In_Progress']
        obj.Finished = data['status']['Finished']
        db.session.commit()
        res = {
                "id":obj.id,
                "task":obj.task,
                "due_by":obj.due_by,
                "status":{
                    "Not_Started":obj.Not_Started,
                    "In_Progress":obj.In_Progress,
                    "Finished":obj.Finished,
                },
            }
        return res,201

@ns.param("due_by","Due Date for Tasks")
@ns.response(404,"No Tasks Found Within Given Due Date!")
@ns.route("/due/<string:due_by>")
class StatusD(Resource):
    @ns.doc("All Todo To Completed in Given Due Date..")
    @ns.marshal_with(todo,code=201)
    def get(self,due_by):
        '''Fetch the Task for Given DueDate..'''
        Obj = Todo.query.filter((Todo.due_by>due_by) & (Todo.Finished==0)).all()
        res = []
        for i in Obj:
            res.append({
                "id":i.id,
                "task":i.task,
                "due_by":i.due_by,
                "status":{
                    "Not_Started":i.Not_Started,
                    "In_Progress":i.In_Progress,
                    "Finished":i.Finished,
                },
            })
        if not Obj:
            api.abort(404,"No Tasks Found To Be  Given Due Date")
        return res,201

@ns.param("due_by","Due Date for Tasks")
@ns.response(404,"No Tasks Found Over Due Date!")
@ns.route("/overdue/<string:due_by>")
class StatusOD(Resource):
    @ns.doc("A Todo with Over Given Due Date..")
    @ns.marshal_with(todo,code=201)
    def get(self,due_by):
        '''Fetch the Task for Given DueDate..'''
        Obj = Todo.query.filter((Todo.due_by<due_by) & (Todo.Finished==0)).all()
        res = []
        for i in Obj:
            res.append({
                "id":i.id,
                "task":i.task,
                "due_by":i.due_by,
                "status":{
                    "Not_Started":i.Not_Started,
                    "In_Progress":i.In_Progress,
                    "Finished":i.Finished,
                },
            })
        if not Obj:
            api.abort(404,"No Tasks Found Over Given Due Date")
        return res,201

@ns.response(404,"No Tasks Finished Yet")
@ns.route("/finished")
class StatusF(Resource):
    @ns.doc("All Tasks Finished till Now..")
    @ns.marshal_with(todo,code=201)
    def get(self):
        '''Fetch All The Tasks That are Finished..'''
        Obj = Todo.query.filter(Todo.Finished==1).all()
        res = []
        for i in Obj:
            res.append({
                "id":i.id,
                "task":i.task,
                "due_by":i.due_by,
                "status":{
                    "Not_Started":i.Not_Started,
                    "In_Progress":i.In_Progress,
                    "Finished":i.Finished,
                },
            })
        if not Obj:
            api.abort(404,"No Tasks Finished Yet..")
        return res,201


if __name__ == '__main__':
    app.run(debug=True)










# class TodoClass(object):
#     def __init__(self):
#         self.todos = []
    
#     def create(self, data):
#         todo = data
#         self.todos.append(todo)
#         return todo
    
#     def get(self,id):
#         for i in self.todos:
#             if i["id"] == id:
#                 return i
#         api.abort(404,f"The task with id : {id} not Found!")

#     def delete(self,id):
#         todo = self.get(id)
#         self.todos.remove(todo)

# Obj = TodoClass()
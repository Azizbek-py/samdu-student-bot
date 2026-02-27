from tinydb import TinyDB, Query, where
from tinydb.database import Document

db1 = TinyDB('details/database/base.json', indent=4)
db2 = TinyDB('details/database/tasks.json', indent=4)
db3 = TinyDB('details/database/student_uploads.json', indent=4)

users = db1.table("Users")
tasks = db2.table("Tasks")
student_uploads = db3.table("Uploads")
query = Query()

def get(table, user_id=None):
    if table == "users":
        if user_id == None:
            return users.all()
        else:
            try:
                return users.get(doc_id=user_id)
            except:
                return None
    if table == "tasks":
        if user_id == None:
            return tasks.all()
        else:
            try:
                return tasks.search(Query().own_of_file == user_id)
            except:
                return None

def get_students_tasks(subject, group=None):
    if group != None:
        try:
            tasks_list = tasks.search(Query().group_data == group)
            filtered = []

            for task in tasks_list:
                for name in task["from_teacher"]["subject_name"]:
                    if name in str(subject):
                        if task not in filtered:
                            filtered.append(task)
            return filtered
        except:
            return None
    else:
        try:
            return tasks.search(where("from_teacher")["subject_name"] == subject)
        except:
            return None

def get_student_uploads(uniq_id=None, user_id=None):
    if user_id == None and uniq_id == None:
        return student_uploads.all()
    
    if user_id != None:
        try:
            doc_id = f"{user_id}{uniq_id}"
            tasks_list = student_uploads.get(doc_id=doc_id) 
            return tasks_list
        except:
            return None
    if user_id == None:
        try:
            tasks_list = student_uploads.search(Query().uniq_id==uniq_id)
            return tasks_list
        except:
            return None



def delete_student_uploads(user_id, uniq_id):
    Student = Query()
    try:
        student_uploads.remove(
        (Student.from_user.user_id == user_id) &
        (Student.uniq_id == uniq_id)
        )
        
        # student_uploads.remove(doc_ids=[f"{user_id}{uniq_id}"])
        return True
    except:
        return False

def insert_student_uploads(user_id, uniq_id, data):
    doc_id = f"{user_id}{uniq_id}"
    try :
        doc = Document(
            value=data,
            doc_id=doc_id
        )
        student_uploads.insert(doc)
        return True
    except:
        return False

def update_student_uploads(id, data):
    student_uploads.update(data, doc_ids=[id])

def insert(table, data, user_id=None):
    if table == "users":
        try:
            doc = Document(
                value=data,
                doc_id=user_id
            )
            users.insert(doc)
        except:
            users.update(data, doc_ids=[user_id])
    if table == "tasks":
        tasks.insert(data)

def upd(table, data, user_id=None):

    if table == "users":
        users.update(data, doc_ids=[user_id])

    if table == "tasks":
        tasks.update(data, doc_ids=[user_id])

def delete(table, user_id=None):
    if table == "users":
        users.remove(doc_ids=[user_id])
    if table == "tasks":
        tasks.remove(Query().uniq_id == user_id)
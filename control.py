#! DataBase !#
import firebase_admin
from firebase_admin import credentials, firestore, db

cred = credentials.Certificate("./databaseKey.json")
firebase_admin.initialize_app(
    cred, {
        "databaseURL":
        "https://urlsrt-f7247-default-rtdb.asia-southeast1.firebasedatabase.app"
    })

#! Functions !#
def DataBaseLoad(data : str):
    ref = db.reference(f"{data}")
    return ref

class Data():
    def dataUpdate(path, *data):
        refPath = db.reference(f"{path}")
        for i in data:
            refPath.update(i)

    def dataGet(path, data):
        refPath = db.reference(f"{path}")
        resultData = refPath.get()[f"{data}"]
        return resultData

    def dataCheck(data):
        refPath = db.reference("USERDATA")
        if refPath.child(str(data)).get() == None: return False
        else: return True

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



def initFirebase():
    # Use the application default credential
    cred = credentials.Certificate("./fast-food-point-comparison-firebase-adminsdk-co2q3-2b004c4a30.json")

    default_app = firebase_admin.initialize_app(cred)


    db = firestore.client()

    
    return db


def setPointData(data):
    doc_ref.set(data)
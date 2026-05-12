import pyrebase


# cred_obj = firebase_admin.credentials.Certificate('....path to file')
# default_app = firebase_admin.initialize_app(cred_object, {
#     'databaseURL':databaseURL
#     })

firebase_config = {
    'apiKey': "AIzaSyCi_pRHNVqZkbcKZgatNENXsqBufsGnOA0",
    'authDomain': "final-fe519.firebaseapp.com",
    'databaseURL': "https://final-fe519-default-rtdb.firebaseio.com",
    'projectId': "final-fe519",
    'storageBucket': "final-fe519.firebasestorage.app",
    'messagingSenderId': "757688929699",
    'appId': "1:757688929699:web:6a5e2083404b8ac7289e16"
}

firebase = pyrebase.initialize_app(firebase_config)
db = None
user = "Hasan"

def connect_to_db():
    global db
    db = firebase.database()

def get_data(key):
    if db is None:
        return None
    data = db.child(f"{user}").child(f"{key}").get()
    return data

def set_data(key, data):
    if db is None:
        return None
    db.child(f"{user}").child(f"{key}").set(data)

def login(username, password):
    pass

def create_account():
    pass

def add_plant():
    pass



# // Import the functions you need from the SDKs you need
# import { initializeApp } from "firebase/app";
# // TODO: Add SDKs for Firebase products that you want to use
# // https://firebase.google.com/docs/web/setup#available-libraries

# // Your web app's Firebase configuration
# const firebaseConfig = {
#   apiKey: "AIzaSyCi_pRHNVqZkbcKZgatNENXsqBufsGnOA0",
#   authDomain: "final-fe519.firebaseapp.com",
#   databaseURL: "https://final-fe519-default-rtdb.firebaseio.com",
#   projectId: "final-fe519",
#   storageBucket: "final-fe519.firebasestorage.app",
#   messagingSenderId: "757688929699",
#   appId: "1:757688929699:web:6a5e2083404b8ac7289e16"
# };

# // Initialize Firebase
# const app = initializeApp(firebaseConfig);
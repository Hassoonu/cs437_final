import pyrebase  # ? install is 'pyrebase4' but import is still 'pyrebase'

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
auth = firebase.auth()   # ? initialize auth once at the top
db   = firebase.database()  # ? no need for connect_to_db() or a global

current_user = None  # stores the logged-in user token object
USERNAME = "Hasan"   # rename to avoid shadowing

def get_data(key):
    data = db.child(USERNAME).child(key).get()
    return data.val()   # ? .val() extracts the actual value; without it you get a pyrebase object

def set_data(key, data):
    db.child(USERNAME).child("money_tree").set(data)

def login(email, password):
    global current_user
    try:
        current_user = auth.sign_in_with_email_and_password(email, password)
        print(f"Logged in as {email}")
    except Exception as e:
        print(f"Login failed: {e}")

def create_account(email, password):
    global current_user
    try:
        current_user = auth.create_user_with_email_and_password(email, password)
        print(f"Account created for {email}")
    except Exception as e:
        print(f"Account creation failed: {e}")

def add_plant(plant_name, plant_data):
    db.child(USERNAME).child(plant_name).set(plant_data)

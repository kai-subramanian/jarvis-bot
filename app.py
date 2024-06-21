import speech_recognition as sr
import google.generativeai as genai
import dotenv
import os
import pyttsx3
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from functools import wraps

dotenv.load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

# Configuration for JWT
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Can be any secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)

# In-memory user store
users = {
   "user1": {"password": "password1", "roles": ["user"]}
}

# In-memory storage for roles
roles_permissions = {
   "user": ["listen","llm"]
}

# Authentication endpoint
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    print(username,"===>",password)
    user = users.get(username)

    if not user or user['password'] != password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity={"username": username, "roles": user['roles']})
    return jsonify(access_token=access_token)

# Authorization decorator
def roles_required(required_roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt_identity()
            user_roles = claims.get('roles', [])
            if any(role in user_roles for role in required_roles):
                return fn(*args, **kwargs)
            return jsonify({"msg": "Access denied"}), 403
        return wrapper
    return decorator

@app.route("/llm", methods=['GET'])
@roles_required(["user"])
def ai_response(my_text="Introduce yourself"):
   engine = pyttsx3.init()
   response = model.generate_content(my_text)
   to_speech = response.text
   print(to_speech)
   engine.say(to_speech)
   engine.runAndWait()
   return jsonify({"message": to_speech})

@app.route("/", methods=['GET'])
@roles_required(["user", "admin"])
def listen():
   text = ""
   recognizer = sr.Recognizer()
   while text != "exit":
      try:
         with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print("You said: " + text)
            ai_response(text)
      except sr.UnknownValueError:
         text = "Could not understand audio"
      except sr.RequestError as e:
         text = "Could not request results from Google Speech Recognition service; {0}".format(e)

   return jsonify({"message": text})

if __name__ == "__main__":
  app.run(debug=True)

This repo contains a takehome assignment done for Helpful Genie. Also attached a video to demo the assignment.

Steps to run - 

1. Clone this repo and go into the directory.
2. Active the venv by doing .\Scripts\activate
3. Kindly substitute the API key for Google Gemini in a .env file, as I have used a placeholder.
4. Run 'flask run' command to start the server.
5. Use Postman to send a POST request to the URL http://127.0.0.1:5000/login to the /login endpoint as a json file, with body as-
   {
     "username":"user1",
     "password":"password1"
   }
   also do kindly set the type as raw and format to json.
6. Now, the response should contain the API key. We can use it to send a request to the server.
7. Send a curl command from another terminal, in this format -> curl -X GET http://localhost:5000/ -H "Authorization: Bearer <paste_api_key_from_step_5_here>"
8. Now, the flask app should start listening, and we can speak to the AI and get the response from it appropriately.
9. We have used Google Gemini 1.5-flash API as the LLM backend, and pyttsx3 engine to convert text to speech.

   Thank you ! :)

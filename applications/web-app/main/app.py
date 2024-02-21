#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def main():
    return '''
     <form action="/echo_user_input" method="POST">
         <input name="user_zip_code">
         <input type="submit" value="Submit">
         <label for="user_zip_code">Zip Code</label><br>
     </form>
     '''

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_zip_code", "")
    return "Your zip code: " + input_text
import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = ""

initial = True

prompt: str = """\n"""

query: str = ""
output_text: str = ""


@app.route("/", methods=("GET", "POST"))
def index():
    global query, prompt, initial, output_text
    if initial:
        initialize()
        initial = False
        return redirect(url_for("index"))
    if request.method == "POST":
        query = query + "\n" + request.form["question"]
        output_text += "\n" + request.form["question"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=query,
            top_p=1,
            temperature=0.9,
            max_tokens=2300,
            frequency_penalty=0.5,
            presence_penalty=0,
        )
        query += "\n" + response.choices[0].text
        output_text += "\r" + response.choices[0].text
        return redirect(url_for("index", result=response.choices[0].text))
    result = request.args.get("result")
    return render_template("index.html", result=result)


def initialize():
    global query, prompt
    query = prompt
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=query,
        top_p=1,
        temperature=0.9,
        max_tokens=2300,
        frequency_penalty=0.5,
        presence_penalty=0,
    )
    return redirect(url_for("index", result=response.choices[0].text))

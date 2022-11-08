from flask import Flask, render_template, request, jsonify
from ner import Parser

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def analyzer():
    if request.method == "POST":
        content = request.form.get("content")
        p = Parser()
        p.load_models("models")
        result = p.predict(content)
        PER = []
        LOC = []
        ORG = []
        for i in result:
            if i[1] == "B-PER":
                PER.append(i[0])
            if i[1] == "I-PER":
                PER[len(PER) - 1] = PER[len(PER) - 1] + " " + i[0]
            if i[1] == "B-LOC":
                LOC.append(i[0])
            if i[1] == "I-LOC":
                LOC[len(LOC) - 1] = LOC[len(LOC) - 1] + " " + i[0]
            if i[1] == "B-ORG":
                ORG.append(i[0])
            if i[1] == "I-ORG":
                ORG[len(ORG) - 1] = ORG[len(ORG) - 1] + " " + i[0]
        SUM = []
        SUM.append(PER)
        SUM.append(LOC)
        SUM.append(ORG)
        return render_template("index.html", data=SUM, content=content)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)

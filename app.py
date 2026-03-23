from flask import Flask, render_template, request, redirect
import pandas as pd
from reportlab.pdfgen import canvas

app = Flask(__name__)

def calculate_pf_esi(salary):
    pf = salary * 0.12
    esi = salary * 0.0075
    return pf, esi

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    salary = float(request.form['salary'])

    pf, esi = calculate_pf_esi(salary)

    data = {"Name": name, "Salary": salary, "PF": pf, "ESI": esi}
    df = pd.DataFrame([data])

    try:
        df.to_csv("employees.csv", mode='a', header=False, index=False)
    except:
        df.to_csv("employees.csv", index=False)

    return redirect('/')

@app.route('/view')
def view():
    try:
        df = pd.read_csv("employees.csv")
        return df.to_html()
    except:
        return "No Data Found"

@app.route('/pdf/<name>/<salary>/<pf>/<esi>')
def pdf(name, salary, pf, esi):
    file_name = f"{name}.pdf"
    c = canvas.Canvas(file_name)

    c.drawString(100, 750, "Salary Slip")
    c.drawString(100, 720, f"Name: {name}")
    c.drawString(100, 700, f"Salary: {salary}")
    c.drawString(100, 680, f"PF: {pf}")
    c.drawString(100, 660, f"ESI: {esi}")

    c.save()
    return "PDF Generated"

def chatbot(query):
    query = query.lower()
    if "pf" in query:
        return "PF is 12%"
    elif "esi" in query:
        return "ESI is 0.75%"
    return "Ask PF or ESI"

@app.route('/chat', methods=['POST'])
def chat():
    q = request.form['query']
    return chatbot(q)

if __name__ == '__main__':
    import os

port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)

from flask import Flask, render_template, request, redirect, url_for
from flask import session
import csv

app = Flask(__name__)
app.secret_key = b'bafe004cc8de79cc96482b95db2d75473a3aa855b3270350267ccc92bddd46c5'

@app.route('/', methods=['GET' , 'POST'])
@app.route("/index", methods=['GET' , 'POST']) 
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        session['numero_gsm'] = request.form['numero_gsm']    
        session['modele_gsm'] = request.form['modele_gsm']
        session['marque_gsm'] = request.form['marque_gsm']
        session['annee_fabrication'] = request.form['annee_fabrication']    
        new_id = None

        with open("data.csv", "r", encoding="utf-8", newline="") as fichier_csv:
            data = list(csv.DictReader(fichier_csv, delimiter=";"))
            new_id = len(data) + 1  

        with open("data.csv", "a", encoding="utf-8", newline="") as fichier_csv:                      
            writer = csv.writer(fichier_csv, delimiter=';')            
            line = [new_id,session['numero_gsm'], session['modele_gsm'], session['marque_gsm'], session['annee_fabrication']]
            writer.writerow(line)
        
        return redirect('/submitted')

@app.route('/submitted')
def submitted():
    return render_template('submitted.html',
                           numero_gsm=session['numero_gsm'],
                           modele_gsm=session['modele_gsm'],
                           redirect=url_for('index'),
                           delay=5000,
                           )

@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    data = []

    with open("/home/vjanssens/revisions/interro_flask/data.csv", "r", encoding="utf-8", newline="") as fichier_csv:
        data = list(csv.DictReader(fichier_csv, delimiter=";"))

    # Search for the dictionary that contains the line to be deleted
    for line in data:
        if line['id'] == id:
            # Remove the dictionary from the list
            data.remove(line)

    # Write the modified list of dictionaries to the CSV file
    with open('/home/vjanssens/revisions/interro_flask/data.csv', mode='w', newline='') as file:
        fieldnames = ['id','numero_gsm', 'modele_gsm', 'marque_gsm', 'annee_fabrication']
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(data)

    return redirect('/')

if __name__ == '__main__':
	app.run(debug=True)

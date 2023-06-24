import pymysql
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lock'

def get_db():
    
         if not hasattr(pymysql, '_connection'):
        pymysql._connection = pymysql.connect()
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
    return pymysql._connection
# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Page de connexion<
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # V�rification des identifiants
        username = request.form['username']
        password = request.form['password']
        
        # Recherchez les informations d'identification dans la base de donn�es
        cur = get_db().cursor()
        cur.execute("SELECT * FROM utilisateurs WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        
        # Redirigez vers la page d'�tat de la laverie si les identifiants sont corrects
        if user:
            return redirect(url_for('laverie'))
        else:
            return render_template('login.html', error='Identifiants incorrects')
    else:
        return render_template('login.html')
@app.route('/inscription', methods=['GET', 'POST'])


def inscription():
    if request.method == 'POST':
        # R�cup�rez les donn�es du formulaire
        nom = request.form['nom']
        prenom = request.form['prenom']
        username = request.form['username']
        password = request.form['password']
        
        # Ins�rez les donn�es dans la base de donn�es
        cur = get_db().cursor()

        cur.execute("INSERT INTO utilisateurs(nom, prenom, username, password) VALUES(%s, %s, %s, %s)", (nom, prenom, username, password))
        mysql.connection.commit()
        cur.close()
        
        # Redirigez vers la page de connexion
        return redirect(url_for('login'))
    else:
        return render_template('inscription.html')



# Page d'�tat de la laverie
@app.route('/laverie')
def laverie():
    # Logique pour r�cup�rer l'�tat de la laverie
    etat_laverie = {'machine_1': 'en fonctionnement', 'machine_2': 'hors service'}
    return render_template('laverie.html', etat_laverie=etat_laverie)
if __name__ == '__main__':
    app.run(host='localhost', port=4450)





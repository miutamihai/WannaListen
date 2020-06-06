from flask import Flask, render_template
import pyodbc

app = Flask(__name__)

conn = pyodbc.connect('DSN=MSSQLServerDatabase;UID=sa;PWD=Mihai16.')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/artisti')
def artists():
    cursor = conn.cursor()
    cursor.execute('select Id, Name, Nationality, CityOfBirth, DateOfBirth, YearOfLaunch from WannaListen.dbo.Artists')
    return render_template('artists.html', data=cursor)


@app.route('/melodii')
def songs():
    cursor = conn.cursor()
    cursor.execute('exec WannaListen.dbo.GetSongsWithArtistName')
    return render_template('songs.html', data=cursor)


@app.route('/autentificare')
def login():
    return render_template('login.html')


@app.route('/inregistrare')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run()

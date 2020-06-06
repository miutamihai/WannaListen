from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

username = ''

conn = pyodbc.connect('DSN=MSSQLServerDatabase;UID=sa;PWD=Mihai16.')


@app.route('/')
def index():
    return render_template('index.html', username=username)


@app.route('/logout/')
def logout():
    global username
    username = ''
    return render_template('index.html', username=username)


@app.route('/artisti/')
def artists():
    print('Artists')
    cursor = conn.cursor()
    cursor.execute('select Id, Name, Nationality, CityOfBirth, DateOfBirth, YearOfLaunch, NumberOfComments from WannaListen.dbo.Artists')
    return render_template('artists.html', data=cursor, username=username)


@app.route('/melodii/')
def songs():
    cursor = conn.cursor()
    cursor.execute('exec WannaListen.dbo.GetSongsWithArtistName')
    return render_template('songs.html', data=cursor, username=username)


@app.route('/autentificare/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        cursor = conn.cursor()
        global username
        username = request.form['username']
        password = request.form['password']
        cursor.execute('select WannaListen.dbo.LoginUser(?, ?)', (username, password))
        res = cursor.fetchone()
        print(res)
        if res[0]:
            return render_template('index.html', username=username)
        else:
            username = ''
            return render_template('failed_login.html')


@app.route('/inregistrare/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        cursor = conn.cursor()
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        cursor.execute('exec WannaListen.dbo.RegisterUser ?, ?, ?', (first_name, last_name, password))
        conn.commit()
        cursor.execute('SELECT TOP 1 GeneratedUserName FROM WannaListen.dbo.Users ORDER BY Id DESC')
        global username
        username = cursor.fetchone()[0]
        return render_template('index.html', username=username)


@app.route('/artist/<int:artist_id>', methods=['GET', 'POST'])
def artist(artist_id):
    if request.method == 'GET':
        cursor = conn.cursor()
        cursor.execute('select Name from WannaListen.dbo.Artists where Id = ?', artist_id)
        artist_name = cursor.fetchone()[0]
        cursor.execute('exec WannaListen.dbo.GetCommentsForArtist ?', artist_id)
        return render_template('artist.html', artist_name=artist_name, username=username, data=cursor)
    else:
        cursor = conn.cursor()
        content = request.form['comment']
        cursor.execute('exec WannaListen.dbo.InsertArtistComment ?, ?, ?', (content, username, artist_id))
        conn.commit()
        cursor.execute('select Name from WannaListen.dbo.Artists where Id = ?', artist_id)
        artist_name = cursor.fetchone()[0]
        cursor.execute('exec WannaListen.dbo.GetCommentsForArtist ?', artist_id)
        return render_template('artist.html', artist_name=artist_name, username=username, data=cursor)


@app.route('/melodie/<int:song_id>', methods=['GET', 'POST'])
def song(song_id):
    if request.method == 'GET':
        cursor = conn.cursor()
        cursor.execute('select Title from WannaListen.dbo.Songs where Id = ?', song_id)
        song_title = cursor.fetchone()[0]
        cursor.execute('exec WannaListen.dbo.GetCommentsForSong ?', song_id)
        return render_template('song.html', song_title=song_title, username=username, data=cursor)
    else:
        cursor = conn.cursor()
        content = request.form['comment']
        cursor.execute('exec WannaListen.dbo.InsertSongComment ?, ?, ?', (content, username, song_id))
        conn.commit()
        cursor.execute('select Title from WannaListen.dbo.Songs where Id = ?', song_id)
        song_title = cursor.fetchone()[0]
        cursor.execute('exec WannaListen.dbo.GetCommentsForSong ?', song_id)
        return render_template('artist.html', song_title=song_title, username=username, data=cursor)


if __name__ == '__main__':
    app.run()

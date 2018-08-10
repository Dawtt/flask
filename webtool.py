from flask import Flask, redirect, url_for, jsonify, request
from p import id_recs_db_controller, artist_song_db_controller
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


subset_path = "/Users/dw/pi/www/flask/p/subset"

db_id = artist_song_db_controller


@app.route("/")
def hello():
	return "Hello Friend, from python flask on pi"


###		ID RELATED SONGS DATABASE CONTROLS

@app.route("/relatedtrack/<trackid>")
def getRelatedTrack(trackid):
	print("so related track is called")
	song_to_return = id_recs_db_controller.getRelatedTrack(trackid)
	print("so back to related track")
	print(type(song_to_return))
	return song_to_return


# @app.route('/result', methods=['GET', 'POST'])
# def result():
# 	trackid = request.args.get('songid', None)
# 	print(type(request))
# 	print(request)
# 	#print(trackid.args)
# 	print(trackid)
# 	print(type(trackid))
# 	if trackid:
# 		return trackid
# 	return "No place information is given"

@app.route('/result', methods = ['GET', 'POST'])
def result():
	if request.method == 'GET':
		place = request.args.get('place', None)
		outputrec = id_recs_db_controller.getRelatedTrack(place)
		print(type(outputrec))
		print(outputrec)
		if outputrec:
			return outputrec
		return "No outputrec information is given"

if __name__ == '__main__':
	app.run(debug = True)


###		ARTIST & TRACKNAME DATABASE CONTROLS

@app.route("/getartistfromid/<trackid>")
def return_artist(trackid):
	artist_to_return = artist_song_db_controller.get_artist_from_track_id(trackid)
	return repr(artist_to_return)

@app.route("/getartistlist/")
def get_artist_list():
	# artists =  meta.get_all_artists()
	# return artists
	artist_list = artist_song_db_controller.get_artists_flask_tut()
	print(type(artist_list))
	artist_list = jsonify(artist_list)
	print(type(artist_list))
	return artist_list

@app.route("/getsongsfromartist/<artist>")
def get_songs_from_artist(artist):
	songs = artist_song_db_controller.get_all_songs_by_artist(artist)
	return repr(songs)


####### 	TESTING ROUTES		#######


@app.route("/dbtest/")
def dbtest():
	id_recs_db_controller.dbTestFunction()
	return "#####	completed dbTestFunction"


@app.route('/admin')
def hello_admin():
	return 'Hello Admin'


@app.route('/guest/<guest>')
def hello_guest(guest):
	return 'Hello %s as Guest' % guest


@app.route('/user/<name>')
def hello_user(name):
	if name =='admin':
		return redirect(url_for('hello_admin'))
	else:
		return redirect(url_for('hello_guest',guest = name))

@app.route("/test/")
def hello2():
	return "This is a test of routing hello2()"


@app.route("/testargs/<section>")
def hello3(section):
	return section



if __name__ == "__main__":
	app.run(debug=True)





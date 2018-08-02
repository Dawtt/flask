
# running server

## quick explanation
dependencies: python3, flask, flask rest-ful
all databases should be in .gitignore - they will need to be manually moved into the project.

correct paths to databases must be entered on both db controllers: `p/id_recs_db_controller.py` & `artist_song_db_controller.py`
run webtool.py to start server

copy files over old ones on the pi & restart apache for production

## detailed

### webtool.py
/flask/webtool.py is basically the entry point here.
 If you run that file in an environment with all python dependencies installed,
 it "should" open up a local webserver accessible from the browser, and note such in the command line.

Don't mess with webtool.wsgi, it's part of the interface with mod_wsgi, which is an apache2 module to run python / flask programs.
so production is basically `apache2 -> mod_wsgi -> webtool.wsgi -> webtool.py -> db controllers`

### paths
database path is currently hardcoded in both db controllers, the db location must be entered.

I keep the pi's path there commented out, to keep it easy to correct when using ssh / command line editing tools to debug

git version control should be set to "ignore" these files, so they will remain where you put them even if you change branches etc. You do not need to worry about git deleting them.)

`flask/p` I only used directory /p to have a short path for using ssh/command line editing on the pi

### testing development html example addresses:
http://127.0.0.1:5000/getsongsfromartist/Jimmy%20McCracklin
http://127.0.0.1:5000/relatedtrack/TREDTHC128F92D42F0
http://127.0.0.1:5000/getartistfromid/TREDTHC128F92D42F0
http://127.0.0.1:5000/getartistlist/
### testing production html addresses:
http://68.168.165.164:10331/flask/getsongsfromartist/Jimmy%20McCracklin
http://dawtt.dynu.net:10331/flask/relatedtrack/TREDTHC128F92D42F0
http://dawtt.dynu.net:10331/flask/getartistfromid/TREDTHC128F92D42F0
http://dawtt.dynu.net:10331/flask/getartistlist/

#### dawtt.dynu.net:10331
dawtt.dynu.net is a dynamic dns service - which in this case just means when my home's router ip address changes, that address will still match. 
Of course my home router only accepts a few specific paid companies with dynamic routing services, so this doesn't actually work dynamically ¯\_(ツ)_/¯
We do need to be mindful in case the router suddenly gets a new ip address from the ISP at a bad time, but mine seems pretty good about providing the same address even when restarting the router.
10331 is the port the router has open for html access, which is forwarded to the pi's ports which are open through it's firewall.

### pycharm / intellij
I have been using pycharm by the jetbrains/intellij people for development here.
I'm using the `venv` virtual environment to make help with dependencies being properly tracked.
You'll need to make sure it has a few things. Note the menu location will probably be slightly different for windows than mac. 

`pycharm/preferences/project/project interpreter` —  it will need:
python 3.5^
Flask
Flask-RESTful
pip

These should trigger it to install other dependencies as well. If you get any import errors, it is probably a dependency needing to be installed.

`pycharm/preferences/languagues & frameworks` — needs:
Flask (make sure the flask integration box is checkmarked_)


### dependencies
I think the only current dependencies needed to install are flask & flask-restful.
Most likely that is wrong of course.
If you add any new dependencies in addition to what there is, they will need to be installed on the pi manually.
It's generally a lot harder to troubleshoot missing dependencies there, so try to keep everyone on the same page.

# GENERAL ISSUES
- debug without pycharm: if you can figure out how to get to non-pycharm debug mode to run correctly (does pycharm just stop it?), let us all know :-)
- little bobby tables: the endpoints for REST requests which make sql queries could probably be used maliciously, need to make sure inputs are sanitized.
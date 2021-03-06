import sqlite3
from contextlib import closing
from flask import Flask, request, g, abort, send_from_directory
from flask.json import jsonify

class VPN:
  def __init__(self, name, latitude, longitude):
    self.name = name
    self.latitude = latitude
    self.longitude = longitude
  
  def distance(self, my_lat, my_long):
    #let's assume cartesian coordinates
    return ((my_lat - self.latitude)**2 + (my_long - self.longitude)**2)**(0.5)
    
DATABASE = '/tmp/gfrog.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

@app.before_request
def before_request():
  g.db = connect_db()

@app.route('/vpn/', methods=['GET'])
def list_vpns():
  if 'mylat' in request.args and 'mylong' in request.args:
    cursor = g.db.execute('SELECT name, latitude, longitude FROM vpn')
    vpns = [VPN(row[0], row[1], row[2]) for row in cursor.fetchall()]
    vpns = sorted(vpns, key=lambda vpn: vpn.distance(float(request.args['mylat']), float(request.args['mylong'])))
    return jsonify(VPNs = [{ 'name': v.name, 'latitude': v.latitude, 'longitude': v.longitude } for v in vpns])
  else:
    abort(400)
  
@app.route('/vpn/<name>', methods=['POST'])
def add_vpn(name):
  if 'lat' in request.form and 'long' in request.form:
    g.db.execute('INSERT INTO vpn (name, latitude, longitude) VALUES (?, ?, ?)',
                [str(name), float(request.form['lat']), float(request.form['long'])])
    g.db.commit()
    return '', 201
  else:
    abort(400)

@app.route('/vpn/<name>', methods=['DELETE'])
def delete_vpn(name):
  g.db.execute('DELETE FROM vpn WHERE name = ?', [str(name)])
  g.db.commit()
  return '', 204

@app.route('/')
def do_test():
  return send_from_directory('static', 'task2test.html')

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        
if __name__ == '__main__':
  app.run(host='0.0.0.0')
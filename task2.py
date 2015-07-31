import sqlite3
from flask import Flask, request, g, abort
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

@app.route('/')
def list_vpns():
  if 'lat' in request.args and 'long' in request.args:
    cursor = g.db.execute('SELECT name, latitude, longitude FROM vpn')
    vpns = [VPN(row[0], row[1], row[2]) for row in cursor.fetchall()]
    vpns = sorted(vpns, key=lambda vpn: vpn.distance(float(request.args['lat']), float(request.args['long'])))
    return jsonify(VPNs = [{ 'name': v.name, 'latitude': v.latitude, 'longitude': v.longitude } for v in vpns])
  else:
    abort(400)
  
@app.route('/add', methods=['GET'])
def add_vpn():
  if 'name' in request.args and 'lat' in request.args and 'long' in request.args:
    g.db.execute('INSERT INTO vpn (name, latitude, longitude) VALUES (?, ?, ?)',
                [str(request.args['name']), float(request.args['lat']), float(request.args['long'])])
    g.db.commit()
    return 'OK'
  else:
    abort(400)

@app.route('/delete', methods=['GET'])
def delete_vpn():
  if 'name' in request.args:
    g.db.execute('DELETE FROM vpn WHERE name = ?', [request.args['name']])
    g.db.commit()
    return 'OK'
  else:
    abort(400)

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        
if __name__ == '__main__':
  app.run(host='0.0.0.0')
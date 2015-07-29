import sqlite3
from flask import Flask, request

app = Flask(__name__)

vpns = []

class VPN:
  def __init__(self, name, latitude, longitude):
    self.name = name
    self.latitude = latitude
    self.longitude = longitude

@app.route('/')
def list_vpns():
  return 'OK'
  
@app.route('/add', methods=['POST'])
def add_vpn():
  if 'name' in request.args and 'lat' in request.args and 'long' in request.args:
    vpns.append(VPN(request.args['name'], request.args['lat'], request.args['long']))

@app.route('/delete', methods=['DELETE'])
def delete_vpn():
  if 'name' in request.args:
    matches_name = lambda n: n.name is not request.args['name']
    vpns = list(filter(matches_name, vpns))

if __name__ == '__main__':
  app.run(host='0.0.0.0')
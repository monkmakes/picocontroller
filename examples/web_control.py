from microdot import Microdot
from network import WLAN, STA_IF
from picocontroller import *
from picocontroller.gui import OLEDConsole

ssid = 'ssid'      # CHANGE ME
password = 'password' # CHANGE ME

index_page = '''
<!DOCTYPE html>
<html>
<head>
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js" type="text/javascript" charset="utf-8"></script>
  <script>
  function set_relay(relay, state){
    $.get('/set-relay?relay='+relay+'&state='+state);
  }
  </script>
</head>
<body>
<table>
    <tr><th>Relay</th>
    <tr><td>A</td>
        <td><input type='button' value='ON' onClick="set_relay('A', '1')"></input></td>
        <td><input type='button' value='OFF' onClick="set_relay('A', '0')"></input></td>
    </tr>
        <tr><td>B</td>
        <td><input type='button' value='ON' onClick="set_relay('B', '1')"></input></td>
        <td><input type='button' value='OFF' onClick="set_relay('B', '0')"></input></td>
    </tr>
        <tr><td>C</td>
        <td><input type='button' value='ON' onClick="set_relay('C', '1')"></input></td>
        <td><input type='button' value='OFF' onClick="set_relay('C', '0')"></input></td>
    </tr>
        <tr><td>D</td>
        <td><input type='button' value='ON' onClick="set_relay('D', '1')"></input></td>
        <td><input type='button' value='OFF' onClick="set_relay('D', '0')"></input></td>
    </tr>
</body>
</html>
'''

console = OLEDConsole()

def connect_wifi(ssid, password):
    wlan = WLAN(STA_IF)
    wlan.active(True)
    console.print('connect: ' + ssid)
    print('connecting to ' + ssid)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('.', end='')
        sleep(1)
    console.print('Connected')
    console.print(str(wlan.ifconfig()[0]))
    print('IP address:', wlan.ifconfig()[0])


app = Microdot()  
connect_wifi(ssid, password)

@app.route('/')
def index(request):
    return index_page, 400, {'Content-Type': 'text/html'}

@app.route('/set-relay')
def temp(request):
    relay = request.args['relay']
    state = int(request.args['state'])
    console.print(relay + ' ' + str(state))
    if relay == 'A':
        Relay_A.value(state)
    elif relay == 'B':
        Relay_B.value(state)
    elif relay == 'C':
        Relay_C.value(state)
    elif relay == 'D':
        Relay_D.value(state)        
    return ""

app.run(port=80)

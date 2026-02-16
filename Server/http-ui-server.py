import http.server
import json
import os
from string import Template
from adc import ADC
from buzzer import Buzzer
from control import Control

PORT = 8888
VOLTAGE_WARN_LIMIT = 6.1
VOLTAGE_CAUTION_LIMIT = 6.9

HTML_TEMPLATE_FILE = 'robot-ui-template.html'

# Initialize hardware controllers
buzzer = Buzzer()
control = Control()

class BatteryRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ('/', '/index.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Read battery levels
            adc = ADC()
            try:
                servo_v, control_v = adc.read_battery_voltage()
            finally:
                adc.close_i2c()
            
            # Determine status colors (Thresholds based on server.py logic)
            servo_color = "#dc3545" if servo_v < VOLTAGE_WARN_LIMIT else "#ddcc00" if servo_v < VOLTAGE_CAUTION_LIMIT else "#28a745"
            control_color = "#dc3545" if control_v < VOLTAGE_WARN_LIMIT else "#ddcc00" if control_v < VOLTAGE_CAUTION_LIMIT else "#28a745"
            
            # Load HTML Template
            template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), HTML_TEMPLATE_FILE)
            with open(template_path, 'r', encoding='utf-8') as f:
                template = Template(f.read())
                
            html = template.substitute(
                servo_color=servo_color,
                control_color=control_color,
                servo_v=f"{servo_v:.2f}",
                control_v=f"{control_v:.2f}"
            )
            self.wfile.write(html.encode('utf-8'))
            
        elif self.path == '/api/battery':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            adc = ADC()
            try:
                servo_v, control_v = adc.read_battery_voltage()
            finally:
                adc.close_i2c()
                
            data = {
                "servo_voltage": servo_v,
                "control_voltage": control_v
            }
            self.wfile.write(json.dumps(data).encode('utf-8'))
            
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/api/buzzer':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            state = data.get('state', False)
            buzzer.set_state(state)
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
            
        elif self.path == '/api/move':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            if data.get('direction') == 'forward':
                # Data format for run_gait: [cmd, gait_mode, x, y, speed, angle]
                # Gait 1 = Tripod, y=10 is forward, speed=5
                move_cmd = ['', '1', '0', '10', '5', '0']
                control.run_gait(move_cmd)
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        else:
            self.send_error(404)

def run(server_class=http.server.HTTPServer, handler_class=BatteryRequestHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Starting battery monitor server on port {PORT}...")
    print(f"Open http://<raspberry-pi-ip>:{PORT} in your browser")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server stopped.")

if __name__ == '__main__':
    run()
import http.server
import json
from adc import ADC

PORT = 8000
VOLTAGE_WARN_LIMIT = 6.1
VOLTAGE_CAUTION_LIMIT = 6.9


class BatteryRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
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
            
            # HTML Template
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Hexapod Battery Monitor</title>
                <meta http-equiv="refresh" content="2">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                        background-color: #f0f2f5;
                        color: #333;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                    }}
                    .card {{
                        background: white;
                        padding: 2rem;
                        border-radius: 12px;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                        text-align: center;
                        min-width: 300px;
                    }}
                    h1 {{ margin-top: 0; color: #333; }}
                    .reading {{
                        margin: 1.5rem 0;
                        padding: 1rem;
                        background: #f8f9fa;
                        border-radius: 8px;
                        border-left: 5px solid #ccc;
                    }}
                    .label {{ display: block; font-size: 0.9rem; color: #666; margin-bottom: 0.5rem; }}
                    .value {{ font-size: 2.5rem; font-weight: bold; }}
                    .unit {{ font-size: 1rem; color: #888; }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>Battery Status</h1>
                    <div class="reading" style="border-left-color: {servo_color}">
                        <span class="label">Servo Power</span>
                        <span class="value" style="color: {servo_color}">{servo_v:.2f}</span> <span class="unit">V</span>
                    </div>
                    <div class="reading" style="border-left-color: {control_color}">
                        <span class="label">Control Power</span>
                        <span class="value" style="color: {control_color}">{control_v:.2f}</span> <span class="unit">V</span>
                    </div>
                </div>
            </body>
            </html>
            """
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
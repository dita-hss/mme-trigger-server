from flask import Flask, request, jsonify
from flask_cors import CORS
from pylsl import StreamInfo, StreamOutlet
import serial
import time

######## Flask setup ########
app = Flask(__name__)
CORS(app)

########Serial setup (Not currenly used) ########
ser = serial.Serial("COM4", 115200, timeout=1)

########LSL stream setup ########
info = StreamInfo(
    name='Trigger',     # stream name / should match AURORAs
    type='Markers',          # stream type
    channel_count=1,
    nominal_srate=0,         # (event-based)
    channel_format='int32', # send string markers 'string / send int markers 'int32'
    source_id='aurora_trigger_01'
)
outlet = StreamOutlet(info)

@app.route("/sendTrigger", methods=["POST"])
def send_trigger():
    data = request.get_json()
    unique_code = data.get("uniqueCode")

    if unique_code is None:
        return jsonify({"error": "Missing uniqueCode"}), 400

    try:
        ####### Send to serial #######
        # command = f"mh{chr(unique_code)}\x00\n"
        # ser.write(command.encode("utf-8"))
        # ser.flush()
        # time.sleep(0.1)
        # print(f"Sent to serial: {repr(command)}")

        ####### Send to LSL #######
        #marker_str = str(unique_code)
        marker_str = unique_code
        outlet.push_sample([marker_str])
        print(f"Sent to LSL: {marker_str}")

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Server running at http://localhost:5000")
    app.run(port=5000)

from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import atexit

app = Flask(__name__)

LED_PIN = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def cleanup_gpio():
    GPIO.cleanup()

atexit.register(cleanup_gpio)

@app.route('/led/on', methods=['GET'])
def turn_on_led():
    GPIO.output(LED_PIN, GPIO.HIGH)
    return jsonify({'status': 'on'}), 200

@app.route('/led/off', methods=['GET'])
def turn_off_led():
    GPIO.output(LED_PIN, GPIO.LOW)
    return jsonify({'status': 'off'}), 200

@app.route('/cpu/temperature', methods=['GET'])
def get_cpu_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_str = f.readline()
            temp_c = int(temp_str) / 1000.0
            return jsonify({'status': 'success', 'unit': 'degree celsius', 'value': temp_c}), 200
    except:
        return jsonify({'status': 'error', 'message': 'thermal sensor is not available'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


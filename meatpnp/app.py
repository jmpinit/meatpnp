import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

machine_lock = threading.Lock()


@app.route('/parts')
def get_parts():
    return jsonify(app.config['MACHINE'].get_part_info())


@app.route("/machine/position")
def get_position():
    x, y = app.config['MACHINE'].position()

    return jsonify({
        'x': x,
        'y': y,
    })


@app.route("/machine/move", methods=['POST'])
def move():
    x = request.args.get('x')
    y = request.args.get('y')

    if x is None or y is None:
        return 'Missing x or y', 400

    with machine_lock:
        app.config['MACHINE'].move_to(float(x), float(y))

    return 'ok'


@app.route("/machine/move/part/<part_name>", methods=['POST'])
def move_to_part(part_name):
    with machine_lock:
        # try:
        app.config['MACHINE'].move_to_part(part_name)
        # except ValueError:
            # return 'Unable to move to part', 400

    return 'ok'


@app.route("/machine/move/left", methods=['POST'])
def move_left():
    step_val = 1

    if 'step' in request.args:
        step = request.args.get('step')

        try:
            step_val = float(step)
        except ValueError:
            return 'Bad step value', 400

    with machine_lock:
        app.config['MACHINE'].move_relative(-step_val, 0)

    return 'ok'


@app.route("/machine/move/right", methods=['POST'])
def move_right():
    step_val = 1

    if 'step' in request.args:
        step = request.args.get('step')

        try:
            step_val = float(step)
        except ValueError:
            return 'Bad step value', 400

    with machine_lock:
        app.config['MACHINE'].move_relative(step_val, 0)

    return 'ok'


@app.route("/machine/move/up", methods=['POST'])
def move_up():
    step_val = 1

    if 'step' in request.args:
        step = request.args.get('step')

        try:
            step_val = float(step)
        except ValueError:
            return 'Bad step value', 400

    with machine_lock:
        app.config['MACHINE'].move_relative(0, step_val)

    return 'ok'


@app.route("/machine/move/down", methods=['POST'])
def move_down():
    step_val = 1

    if 'step' in request.args:
        step = request.args.get('step')

        try:
            step_val = float(step)
        except ValueError:
            return 'Bad step value', 400

    with machine_lock:
        app.config['MACHINE'].move_relative(0, -step_val)

    return 'ok'


@app.route("/machine/anchor/<label>", methods=['POST'])
def set_anchor(label):
    if label == 'upper_left':
        with machine_lock:
            app.config['MACHINE'].set_upper_left_position()
    elif label == 'upper_right':
        with machine_lock:
            app.config['MACHINE'].set_upper_right_position()
    elif label == 'lower_left':
        with machine_lock:
            app.config['MACHINE'].set_lower_left_position()
    elif label == 'lower_right':
        with machine_lock:
            app.config['MACHINE'].set_lower_right_position()
    else:
        return 'Unrecognized label', 400

    return 'ok'

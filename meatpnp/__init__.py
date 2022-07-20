from machine import MeatPnP
from app import app
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=str, help='Serial port path')
    parser.add_argument('--parts', type=str, help='CSV file containing part positions exported from KiCad')

    args = parser.parse_args()

    port_path = args.port
    parts_filename = args.parts

    # # app.config['MACHINE'] = MeatPnP(parts_filename, '/dev/tty.usbmodem1701')
    app.config['MACHINE'] = MeatPnP(parts_filename, port_path)
    #
    # # It isn't safe to use the reloader in a thread
    app.run(host='0.0.0.0', debug=True, use_reloader=False)


if __name__ == '__main__':
    main()

# Meat PnP

This is bad code that was lazily hacked together for the purposes explained
here: https://hackaday.io/project/186411-meat-pnp

## Usage

Use KiCad to export part centroids in CSV format with the following columns:

* Ref
* Val
* Package
* PosX
* PosY
* Rot
* Side

Start the server and initialize the machine by running the following:

```
python3 meatpnp/__init__.py --port /dev/tty.foobar --parts "parts.csv"
```


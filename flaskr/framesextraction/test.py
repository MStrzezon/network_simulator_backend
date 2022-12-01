import json

from pysondb import db

from flaskr.model.frame import FrameSchema

frames_string = """{
    "devices": [
        {
            "name": "alfa",
            "lat": 50.065607816004639,
            "lon": 19.9155651840895,
            "alt": 3
        },
        {
            "name": "blonia",
            "lat": 50.060667559992207,
            "lon": 19.909718523873616,
            "alt": 1
        },
        {
            "name": "D13",
            "lat": 50.070749606821,
            "lon": 19.90674912815427,
            "alt": 2
        }
    ],
    "packets": [
        {
            "source": "D13",
            "destination": "blonia",
            "rssi": -132.52,
            "snr": -21.62,
            "duration": 0.165,
            "calculated_ber": 0.000001,
            "payload": "hello",
            "packet_type": null,
            "lost": true
        },
        {
            "source": "D13",
            "destination": "alfa",
            "rssi": -122.371,
            "snr": -11.49,
            "duration": 0.165,
            "calculated_ber": 0.001,
            "payload": "hello",
            "packet_type": null,
            "lost": false
        }
    ],
    "links": [
        {
            "source": "D13",
            "destination": "alfa"
        }
    ]
}"""

frames = json.loads(frames_string)

frames_db = db.getDb('frames.json')


frame = FrameSchema().load(frames)
frames_db.add(frame)
import logging

from simpy import core, Store

import flaskr.lorameshsimulator.layer0.utils as utils

logger = logging.getLogger('sim')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


class RadioEnvironment(object):
    SF = 10
    HEADER = 11
    BW = 0.125
    FREQ = 868

    def __init__(self, env, capacity=core.Infinity):
        self.env = env
        self.capacity = capacity
        self.pipes = []

    def tx(self, value):
        if not self.pipes:
            raise RuntimeError('There are no output pipes.')
        events = [store.put(value) for store in self.pipes]
        return self.env.all_of(events)

    def rx(self):
        pipe = Store(self.env, capacity=self.capacity)
        self.pipes.append(pipe)
        return pipe


class PhysicalLayer:
    def __init__(self, name, env, rf, out):

        self.id = name
        self.env = env
        self.geo = None
        self.out = out

        self.rf = rf
        self.rf_pipe = rf.rx()
        self.env.process(self._rx_listener())

        self.received = []
        self.tx_power = 14
        self.rx_mode = False

    def tx(self, data):
        time_toa = utils.toa(len(data) + self.rf.HEADER, self.rf.SF)
        self._log(data, state="transmitted")

        self.rf.tx({"time_begin": self.env.now,
                    "time_toa": time_toa,
                    "sender": self,
                    "payload": data})
        self.out.add_packet(self.env.now, {"source": self.id}, 0)

        yield self.env.timeout(time_toa)

    def rx(self, timeout):
        self.rx_mode = True
        yield self.env.timeout(timeout)
        self.rx_mode = False

        buffer = self.received
        self.received = []
        return buffer

    def rx_one(self, timeout):
        self.rx_mode = True
        for _ in range(1, timeout):
            yield self.env.timeout(1)
            if self.received:
                self.rx_mode = False
                buffer = self.received
                self.received = []
                yield self.env.timeout(2)
                return buffer

        return []

    def _rx_listener(self):
        while True:
            msg = yield self.rf_pipe.get()

            if self.rx and msg["time_begin"] == self.env.now:

                if msg["sender"] == self:
                    continue

                link = utils.BudgetLinkCalculator(msg["sender"].geo, self.geo)

                msg = {'sender': msg["sender"].id,
                       'rssi': link.calculate_rssi(msg["sender"].tx_power),
                       'snr': link.calculate_snr(msg["sender"].tx_power),
                       'toa': msg['time_toa'],
                       'payload': msg["payload"]}
                msg['lost'] = utils.monte_carlo(self.rf.SF, msg['snr'], len(msg['payload']) + self.rf.HEADER)

                yield self.env.timeout(msg["toa"])

                if self.rx:
                    self.received.append(msg)
                    packet = msg.copy()
                    self.out.add_packet(self.env.now, {
                        "tx": packet["sender"],
                        "rx": self.id,
                        "source": packet['payload']["from"],
                        "destination": packet['payload']["dest"],
                        "hops": [str(hop) for hop in packet['payload']["hops"]],
                        "rssi": packet['rssi'],
                        "snr": packet['snr'],
                        "duration": packet['toa'],
                        "payload": packet['payload']['payload'],
                        "lost": packet['lost']
                    }, packet['toa'])

                    if packet['lost']:
                        self._log(msg['payload'], state="lost\t")
                    else:
                        self._log(msg['payload'], state="received")

    def _log(self, msg, state="", warn=False):
        log = logger.warning if warn else logger.info
        log("[%07.3fs @ %s]\t%s\t%s", self.env.now / 1000, self.id.rjust(7), state, msg)

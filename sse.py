import queue


class MessageAnnouncer:

    def __init__(self):
        self.listeners = []

    def listen(self):
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        return q

    def announce(self, msg):
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]


announcer = MessageAnnouncer()


def format_sse(data: str, event=None) -> str:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg


def sendStatus(motorsSpeed, ledStatus, startTime):
    
    if ledStatus:
        ledStatus = "enabled"
    else:
        ledStatus= "disabled"

    msg = format_sse("speed=" + str(motorsSpeed) + ",ledStatus=" + ledStatus + ",startTime=" + str(startTime))
    announcer.announce(msg=msg)
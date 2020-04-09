import pika


class ConnectionHandler(object):
    @property
    def connection(self):
        if self._connection is None:
            self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self._host)
        )
        return self._connection

    def __init__(self, host):
        self._host = host
        self._connection = None # Lazy Init

    def get_connection(self):
        """
        :rtype: pika.BlockingConnection
        """
        return self.connection


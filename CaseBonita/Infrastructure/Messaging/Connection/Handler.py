import pika


class ConnectionHandler(object):
    def _generate_connection(self):
        return pika.BlockingConnection(
            pika.ConnectionParameters(host=self._host)
        )

    def _restart_connection(self):
        self._connection.close()
        self._connection = self._generate_connection()

    @property
    def connection(self):
        if self._connection is None:
            self._connection = self._generate_connection()
        if not self._connection.is_open:
            self._restart_connection()
        return self._connection

    def __init__(self, host):
        self._host = host
        self._connection = None # Lazy Init

    def get_connection(self):
        """
        :rtype: pika.BlockingConnection
        """
        return self.connection


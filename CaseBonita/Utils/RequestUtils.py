import logging
import time
from functools import wraps


class RetryDecorator:
    """
    This class is used to retry requests at an API/Web page.
    Use the main method as a decorator on any request call you wish.
    ** Some more testing is required **
    """
    logger = logging.getLogger(__name__)

    @classmethod
    def main(cls, exceptions, total_retries=4, initial_wait=0.5, backoff=2, logger=None):
        """
        calling the decorated function applying an exponential backoff.

        exceptions: Exception(s) that trigger a retry, can be a tuple
        total_tries: Total tries
        initial_wait: Time to first retry
        backoff: Backoff multiplier (e.g. value of 2 will double the delay each retry).
        logger: logger to be used, if none specified print
        """

        def retry_decorator(f):
            @wraps(f)
            def retries(*args, **kwargs):
                tries, delay = total_retries + 1, initial_wait
                while tries > 1:
                    try:
                        cls.log(f'{total_retries + 2 - tries}. try:', logger)
                        return f(*args, **kwargs)
                    except exceptions as e:
                        tries -= 1
                        print_args = args if args else 'no args'
                        if tries == 1:
                            msg = str(f'Function: {f.__name__}\n'
                                      f'Failed despite best efforts after {total_retries} tries.\n'
                                      f'args: {print_args}, kwargs: {kwargs}')
                            cls.log(msg, logger)
                            raise
                        msg = str(f'Function: {f.__name__}\n'
                                  f'Exception: {e}\n'
                                  f'Retrying in {delay} seconds!, args: {print_args}, kwargs: {kwargs}\n')
                        cls.log(msg, logger)
                        time.sleep(delay)
                        delay *= backoff

            return retries

        return retry_decorator

    @classmethod
    def log(cls, msg, logger=None):
        if logger:
            logger.warning(msg)
        print(msg)


def retry_request(exceptions=None, total_retries=3):
    """
    :rtype: Requests retry Decorator Object
    """
    exceptions = exceptions or Exception
    return RetryDecorator.main(exceptions, total_retries=total_retries, logger=RetryDecorator.logger)

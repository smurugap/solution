import logging
import logging.handlers
from sys import stderr, stdout

SYSLOG_SERVER = '10.87.70.18'
SYSLOG_PORT = 514
if not '_loggers' in locals():
    _loggers = {}

def getLogger(name, execution_id='test'):
    if name not in _loggers:
        _loggers[name] = Logger(name, execution_id)
    return _loggers[name].logger

class Logger(object):
    def __init__(self, name, execution_id):
        logger = logging.getLogger(name)
        formatter = logging.Formatter('%(levelname)-5s %(exec_id)s %(name)s: %(message)s')
        handler = logging.StreamHandler(stream=stdout)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        if SYSLOG_SERVER:
            extra = {'exec_id': execution_id}
            handler = logging.handlers.SysLogHandler(address=(SYSLOG_SERVER, SYSLOG_PORT))
            handler.setFormatter(formatter)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)
        logger = logging.LoggerAdapter(logger, extra)
        self.logger = logger

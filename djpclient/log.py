
import logging


class DJPHandler(logging.Handler):
    
    def emit(self, record):
        import actions
        actions.TransmitLogMessage(record)


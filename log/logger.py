import logging

def return_logger():
    logging.basicConfig(filename='./log/output.log')

    logging.root.setLevel(logging.NOTSET)

    logging.basicConfig(level=logging.NOTSET)

    logger = logging.getLogger("logger_request")
    
    return logger
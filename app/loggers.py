import logging


logger = logging.getLogger("tournaments")
ch = logging.StreamHandler()
ch.setFormatter(
    logging.Formatter(
        fmt="%(asctime)s %(filename)s:%(lineno)d [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ),
)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

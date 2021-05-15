import logging


def setup_logger(name, log_file, level=logging.INFO):
    """
    Initialize logging files
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.propagate = False
        formatter = logging.Formatter(
            "%(levelname)s: %(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
        )
        Handler = logging.FileHandler(log_file, mode="a")

        Handler.setFormatter(formatter)
        logger.setLevel(level)
        logger.addHandler(Handler)


def logger(msg, level, logfile):
    """
    Used for real time logging
    """
    if logfile == "info":
        log = logging.getLogger("log_info")
    if logfile == "error":
        log = logging.getLogger("log_error")
    if logfile == "time_elapsed":
        log = logging.getLogger("log_time")
    if logfile == "token":
        log = logging.getLogger("token_logs")

    log.propagate = False
    if level == "info":
        log.info(msg)
    if level == "warning":
        log.warning(msg)
    if level == "error":
        log.error(msg)

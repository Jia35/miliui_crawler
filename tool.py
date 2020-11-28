import logging


def set_logger():
    """設定 Log 記錄檔"""
    logger = logging.getLogger()
    logger.setLevel(level=logging.INFO)

    handler = logging.FileHandler('miliui.log', mode='a', encoding='utf-8')
    formatter = logging.Formatter(
        fmt='%(asctime)s: %(levelname)s: %(lineno)d: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    console = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger

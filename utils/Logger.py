import logging
from logging import handlers


class Logger(object):
    """
    create Logger use logging
    """

    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, filename, log_to_file=False, level='info', when='D', back_count=3,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        """
        create Logger with file name.
        Args:
            filename: Logger file name
            level: default log level
            when: interval time of log file: S 秒, M 分, H 小时, D 天, W 每星期（interval==0时代表星期一), midnight 每天凌晨
            back_count: backup files limit
            fmt: format of log
        """
        self._filename = filename
        self.logger = logging.getLogger(self._filename)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)
        self.logger.addHandler(sh)
        if log_to_file:
            th = handlers.TimedRotatingFileHandler(filename=self._filename, when=when,
                                                   backupCount=back_count, encoding='utf-8')
            th.setFormatter(format_str)
            self.logger.addHandler(th)

    def getLogger(self):
        return logging.getLogger(self._filename)

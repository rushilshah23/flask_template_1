import datetime
import logging
import logging.handlers
import os


class ProductionLogger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Console handler to show all messages
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)


        # Ensure the logs directory exists
        daily_logs = './logs/daily_logs'
        app_logs = './logs/app_logs'
        if not os.path.exists(daily_logs):
            os.makedirs(daily_logs)
        if not os.path.exists(app_logs):
            os.makedirs(app_logs)


        # Rotating file handler to store warnings and above
        file_handler = logging.handlers.RotatingFileHandler(os.path.join(app_logs, 'app.log'), maxBytes=1024*1024, backupCount=5)
        file_handler.setLevel(logging.INFO)
        # Create a formatter
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)


        # Tim Rotating file handler to store warnings and above
        time_file_handler = logging.handlers.TimedRotatingFileHandler(os.path.join(daily_logs, f'{datetime.datetime.now().date()}.log'),when='midnight', interval=1, backupCount=365)
        time_file_handler.setLevel(logging.INFO)
        # Create a formatter
        time_file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        time_file_handler.setFormatter(time_file_formatter)


        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(time_file_handler)



    def log_debug(self, message):
        self.logger.debug(message)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_critical(self, message):
        self.logger.critical(message)

# Usage
# if __name__ == "__main__":
#     logger = ProductionLogger()
#     logger.log_debug("Just a debug message to log on the console")
#     logger.log_warning('This is a warning message')
#     logger.log_error('This is an error message')
#     logger.log_critical('This is a critical message')



app_logger = ProductionLogger()
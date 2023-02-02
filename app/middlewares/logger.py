from flask import Flask
import logging.config
import yaml


class Logger:
    """
    # Middleware do logging.
    """

    @classmethod
    def init_app(cls, app: Flask) -> None:
        """
        # Registra o middleware no app.
        """
        with open("./logging.yaml", "r") as config_file:
            logging.config.dictConfig(yaml.load(config_file, Loader=yaml.FullLoader))

        app.logger = logging.getLogger(__name__)

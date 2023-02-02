from flask import Flask
from .blueprint import Blueprint
from .logger import Logger


def configure_middlewares(app: Flask) -> None:
    """
    # Configura os middlewares da aplicação.
    """
    Blueprint.init_app(app)
    Logger.init_app(app)

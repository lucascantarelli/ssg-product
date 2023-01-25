from flask import Flask
from app.common import COMMON_ROUTES


class Blueprint:
    """
    # Classe responsável pelo registro das rotas
    """

    @classmethod
    def init_app(cls, app: Flask) -> None:
        """
        # Registra as rotas no app.
        """
        app.register_blueprint(COMMON_ROUTES.COMMON_BP)

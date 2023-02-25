import os
from flask import Flask
from app.middlewares import configure_middlewares
from dotenv import load_dotenv


class App(Flask):
    """
    # Classe responsável pela criação da aplicação.
    """

    def __init__(self) -> None:
        """
        # ? Inicializa o aplicativo flask.
        # ? Invoca o metodo init da classe mãe.
        # ? Verifica o ambiente do app e carrega as configs.
        """
        super().__init__(
            __name__,
            template_folder=os.path.abspath('app'),
            static_folder=os.path.abspath('app/dist'),
        )
        # App recebe a própria instancia.
        self.app = self
        # Carrega as variaveis do ambiente da aplicação.
        load_dotenv()
        # Configura os middlewares
        configure_middlewares(self.app)

    def get_app(self) -> Flask:
        """
        # Retorna a instancia da aplicação.
        """
        return self.app

import os
from flask import Flask
from app.middlewares import Blueprint


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
            static_folder=os.path.abspath('app/templates/dist'),
        )
        # App recebe a própria instancia.
        self.app = self
        # Verifica o ambiente do app e carrega as configs.
        self.env = os.environ.get('APP_ENV', 'Development')
        # Carrega as informações de health check.
        self.health = self.health_check()
        # Configura os middlewares
        self.__configure_middlewares()

    def __configure_middlewares(self) -> None:
        """
        # Configura os middlewares da aplicação.
        """
        Blueprint.init_app(self.app)

    def create_app(self) -> Flask:
        """
        # Retorna a instancia da aplicação.
        """

        return self.app
        
    def health_check(self) -> dict:
        """
        # Retorna o status da aplicação.
        """ 
        return {
            "status": "OK",
            "message": "Application is running.",
            "version": "0.0.0",
            "environment": self.env
        }

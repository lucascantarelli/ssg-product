from flask import Blueprint

class CommonRoutes:
    """
    # Classe responsável por gerenciar as rotas comuns.
    """

    # Cria o blueprint de autenticação.
    COMMON_BP = Blueprint('common_bp', __name__, url_prefix='/')

    @COMMON_BP.route('/', methods=['GET'])
    def index() -> str:
        """
        # Retorna a página inicial.
        """

        return 'Hello World'
        
    @COMMON_BP.route('/health', methods=['GET'])
    def health_check() -> dict:
        """
        # Retorna o status da aplicação.
        """
        app_status = {
            "status": "OK",
            "message": "Application is running.",
            "version": "0.0.0",
            "environment": "dev"
        }
        #logging.info("health check", extra=app_status)
        return app_status

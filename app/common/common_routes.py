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

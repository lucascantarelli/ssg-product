class AppTest:
    """
    # Classe de testes da aplicação.
    """

    def test_app_health_check(self, client) -> None:
        """
        # Testa o health check da aplicação.
        """
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json == {
            "status": "OK",
            "message": "Application is running.",
            "version": "0.0.0",
            "environment": "dev"
        }

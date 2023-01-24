from flask import Flask


class App(Flask):

    @staticmethod
    def create_app():
        app = App(__name__)

        @app.route('/')
        def hello_world():
            return 'Hello, World!'

        return app

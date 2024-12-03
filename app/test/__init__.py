from .connection_test import test_bp

def register_test_routes(app):
    app.register_blueprint(test_bp, url_prefix='/test')

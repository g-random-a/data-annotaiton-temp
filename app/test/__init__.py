from .connection_test import test_bp
from .rabbitmq_test import test_R_MQQT_bp

def register_test_routes(app):
    app.register_blueprint(test_bp, url_prefix='/test')
    app.register_blueprint(test_R_MQQT_bp, url_prefix='/testmqtt')

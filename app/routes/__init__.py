from .upload import upload_bp
from .annotate import annotate_bp

def register_routes(app):
    app.register_blueprint(upload_bp, url_prefix='/api')
    app.register_blueprint(annotate_bp, url_prefix='/api')


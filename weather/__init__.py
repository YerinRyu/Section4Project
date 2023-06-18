from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['TIMEOUT'] = 100000
    
    # blueprint
    from weather.views import main_views, clothes_views, weather_views, dashboard
    app.register_blueprint(main_views.bp)
    app.register_blueprint(clothes_views.bp)
    app.register_blueprint(weather_views.bp)
    app.register_blueprint(dashboard.bp)

    return app
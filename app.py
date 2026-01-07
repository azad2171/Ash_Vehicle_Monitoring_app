from flask import Flask
from flask_migrate import Migrate
from database import db
from flask import render_template

migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from routes.trucks import truck_bp
    from routes.gates import gate_bp
    from routes.dashboard import dashboard_bp
    from routes.weighbridge import weighbridge_bp

    app.register_blueprint(truck_bp)
    app.register_blueprint(gate_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(weighbridge_bp)

    from flask import redirect

    @app.route("/")
    def home():
        return render_template("home.html")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secreat that should be overridden by instance config
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it existing, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config, if it existing, when not testing
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello,Horld!'

    # register the database commands
    from . import db
    print(db.init_app)
    db.init_app(app)

    #register blueprint
    from . import auth
    from . import blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app

import os
from flask import Flask, request, abort
from flask_cors import CORS
from models import setup_db, Movies, Actors
from auth import AuthError, requires_auth
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def create_app(test_config=None, test=False):
    # create and configure the app
    app = Flask(__name__)
    CORS(app, resources={r"/": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS'
        )
        return response

    if test:
        db_path = "test_casting"
    else:
        db_path = "casting"

    db = setup_db(app, f"postgres://henry.dashwood@localhost:5432/{db_path}")

    @app.route('/', methods=['GET'])
    def hello():
        return {"hello": "hello world"}

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(headers):
        try:
            movies = db.session.query(Movies).all()
            movies = [m.format() for m in movies]
            return {
                "success": True,
                "movies": movies
            }
        except:
            db.rollback()
            abort(404)
        finally:
            db.session.close()

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(headers):
        try:
            actors = db.session.query(Actors).all()
            actors = [a.format() for a in actors]
            return {
                "success": True,
                "actors": actors
            }
        except:
            db.session.rollback()
            abort(404)
        finally:
            db.session.close()

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def create_movie(headers):
        try:
            payload = request.get_json()
            movie = Movies(
                title=payload['title'],
                release_date=payload['release_date']
            )
            db.session.add(movie)
            db.session.commit()
            return {
                "success": True,
                "movie": movie.format()
            }
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def create_actor(headers):
        try:
            payload = request.get_json()
            actor = Actors(
                name=payload['name'],
                age=payload['age'],
                gender=payload['gender']
            )
            db.session.add(actor)
            db.session.commit()
            return {
                "success": True,
                "actor": actor.format()
            }
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(headers, id):
        try:
            payload = request.get_json()
            movie = db.session.query(Movies).get(id)
            movie.title = payload['title']
            movie.release_date = payload['release_date']
            db.session.commit()
            return {
                "success": True,
                "movie": movie.format()
            }
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_actor(headers, id):
        try:
            payload = request.get_json()
            actor = db.session.query(Actors).get(id)
            actor.name = payload['name']
            actor.age = payload['age']
            actor.gender = payload['gender']
            db.session.commit()
            return {
                "success": True,
                "actor": actor.format()
            }
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(headers, id):
        try:
            movie = db.session.query(Movies).filter(
                Movies.id == id).one_or_none()
            if movie is None:
                abort(404)
            db.session.delete(movie)
            db.session.commit()
            return {
                "success": True,
                "movie": movie.format()
            }
        except Exception as e:
            print(e)
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(headers, id):
        try:
            payload = request.get_json()
            actor = db.session.query(Actors).filter(
                Actors.id == id).one_or_none()
            if actor is None:
                abort(404)
            db.session.delete(actor)
            db.session.commit()
            return {
                "success": True,
                "actor": actor.format()
            }
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.errorhandler(400)
    def bad_request(error):
        return {
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }, 400

    @app.errorhandler(404)
    def not_found(error):
        return {
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }, 404

    @app.errorhandler(405)
    def not_allowed(error):
        return {
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }, 405

    @app.errorhandler(422)
    def unprocessable(error):
        return {
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }, 422

    return app

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        """
        Receive the raised authorization error and propagates it as response
        """
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

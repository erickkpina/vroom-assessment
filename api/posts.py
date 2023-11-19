from flask import jsonify, Blueprint
from blueprints.posts.models import Posts
from api import api_blueprint


@api_blueprint.route('/get_posts', methods=['GET'])
def get_posts():
    posts = Posts.query.order_by(Posts.date_posted).all()

    if not posts:
        return jsonify({'message': 'No posts found!'}), 404

    serialized_posts = [post.serialize() for post in posts]

    return jsonify(serialized_posts), 200



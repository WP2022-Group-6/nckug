from flask import abort, jsonify, request
from flask_login import login_required, current_user

from flaskr.models import User, UsersWithoutVerify, Group, UserGroup, Transaction, UserTransaction, TransactionMessage, Post, PostComment, Like, Collection
from flaskr import app, socketio


def isempty(*args: str) -> bool:
    for arg in args:
        if len(arg) == 0 or arg.isspace():
            return True
    return False


@app.route('/api/post/new-post', methods=['POST'])
@login_required
def new_post():
    title = request.values.get('title', '')
    content = request.values.get('content', '')

    if isempty(title, content):
        abort(400)

    data = {'post_id': None}

    post = Post.create(user_id=current_user.id, title=title, content=content)
    data['post_id'] = post.id

    socketio.emit('update')

    return jsonify(data)


@app.route('/api/post/get-post', methods=['GET'])
@login_required
def get_post():
    amount = request.args.get('amount', '')
    collection = request.args.get('collection', '')

    try:
        amount = (int(amount) if int (amount) >= 0 else 0) if not isempty(amount) else 0
    except:
        abort(400)

    data = []

    if collection != 'True':
        for post in (Post.query.all() or []):
            like_amount = Like.query.filter_by(_post_id=post.id).count()
            collection_amount = Collection.query.filter_by(_post_id=post.id).count()
            owner = User.query.get(post.user_id)
            temp_post = {'post_id': post.id, 'title': post.title, 'owner': owner.name, 'content': post.content, 'comment': [],
                         'like_amount': like_amount, 'collection_amount': collection_amount, 'comment_amount': None}
            temp_post['like'] = (Like.query.filter_by(_post_id=post.id, _user_id=current_user.id).first() is not None)
            temp_post['collect'] = (Collection.query.filter_by(_post_id=post.id, _user_id=current_user.id).first() is not None)
            for comment in (PostComment.query.filter_by(_post_id=post.id).all() or []):
                user = User.query.get(comment.user_id)
                temp_post['comment'].append({'user_name': user.name, 'content': comment.content})
            temp_post['comment_amount'] = len(temp_post['comment'])
            data.append(temp_post)
            if amount and len(data) == amount:
                break
    else:
        for collection in (Collection.query.filter_by(_user_id=current_user.id).all() or []):
            post = Post.query.get(collection.post_id)
            like_amount = Like.query.filter_by(_post_id=post.id).count()
            collection_amount = Collection.query.filter_by(_post_id=post.id).count()
            owner = User.query.get(post.user_id)
            temp_post = {'post_id': post.id, 'title': post.title, 'owner': owner.name, 'content': post.content, 'comment': [],
                         'like_amount': like_amount, 'collection_amount': collection_amount, 'comment_amount': None}
            temp_post['like'] = (Like.query.filter_by(_post_id=post.id, _user_id=current_user.id).first() is not None)
            temp_post['collect'] = (Collection.query.filter_by(_post_id=post.id, _user_id=current_user.id).first() is not None)
            for comment in (PostComment.query.filter_by(_post_id=post.id).all() or []):
                user = User.query.get(comment.user_id)
                comment_info = {'user_name': user.name, 'content': comment.content}
                temp_post['comment'].append(comment_info)
            temp_post['comment_amount'] = len(temp_post['comment'])
            data.append(temp_post)
            if amount and len(data) == amount:
                break

    return jsonify(data)


@app.route('/api/post/new-response', methods=['POST'])
@login_required
def new_response():
    post_id = request.values.get('post_id', '')
    like = request.values.get('like', '')
    collection = request.values.get('collection', '')

    try:
        post_id = int(post_id)
        post = Post.query.get(post_id)
    except:
        abort(400)

    if not post:
        abort(400)

    data = False

    if like == 'True' and not Like.query.filter_by(_post_id=post_id, _user_id=current_user.id).first():
        Like.create(post_id=post_id, user_id=current_user.id)
        data = True
    if like == 'False' and Like.query.filter_by(_post_id=post_id, _user_id=current_user.id).first():
        post_resp = Like.query.filter_by(_post_id=post_id, _user_id=current_user.id).first()
        post_resp.remove()
        data = True

    if collection == 'True' and not Collection.query.filter_by(_post_id=post_id, _user_id=current_user.id).first():
        Collection.create(post_id=post_id, user_id=current_user.id)
        data = True
    if collection == 'False' and Collection.query.filter_by(_post_id=post_id, _user_id=current_user.id).first():
        post_resp = Collection.query.filter_by(_post_id=post_id, _user_id=current_user.id).first()
        post_resp.remove()
        data = True

    socketio.emit('update')

    return jsonify(data)


@app.route('/api/post/new-comment', methods=['POST'])
@login_required
def new_comment():
    post_id = request.values.get('post_id', '')
    content = request.values.get('content', '')

    try:
        post_id = int(post_id)
        post = Post.query.get(post_id)
    except:
        abort(400)

    if isempty(content) or not post:
        abort(400)

    PostComment.create(post_id=post_id, user_id=current_user.id, content=content)

    socketio.emit('update')

    return jsonify(True)

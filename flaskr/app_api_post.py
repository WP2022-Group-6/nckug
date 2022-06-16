from flask import abort, jsonify, request
from flask_login import login_required, current_user

from flaskr.models import User, UsersWithoutVerify, Group, UserGroup, Transaction, UserTransaction, TransactionMessage, Post, PostComment, Like, Collection
from flaskr import app


def isempty(*args: str) -> bool:
    for arg in args:
        if len(arg) == 0 or arg.isspace():
            return True
    return False


def istrue(arg: str) -> bool:
    if arg == str(True):
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

    return jsonify(data)


@app.route('/api/post/get-post', methods=['GET'])
@login_required
def get_post():
    amount = request.args.get('amount', None)
    collection = request.args.get('collection', None)

    if amount:
        try:
            amount = int(amount)
        except:
            abort(400)
    if collection:
        if collection in ['True', 'False']:
            collection = istrue(collection)
        else:
            abort(400)

    data = []

    if not collection:
        amount_count = 0
        for post in (Post.query.all() or []):
            like_amount = Like.query.filter_by(_post_id=post.id).count()
            collection_amount = Collection.query.filter_by(_post_id=post.id).count()
            temp_post = {'post_id': post.id, 'title': post.title, 'content': post.content, 'comment': [],
                         'like_amount': like_amount, 'collection_amount': collection_amount, 'comment_amount': None}
            comment_list = PostComment.query.filter_by(_post_id=post.id).all()
            count = 0
            for comment in (comment_list or []):
                count += 1
                user = User.query.get(comment.user_id)
                temp_post['comment'].append({'user_name': user.name, 'content': comment.content})
            temp_post['comment_amount'] = count
            data.append(temp_post)
            amount_count += 1
            if amount is not None:
                if (amount_count == amount):
                    break
    else:
        amount_count = 0
        for collection in (Collection.query.filter_by(_user_id=current_user.id).all() or []):
            post = Post.query.get(collection.post_id)
            like_amount = Like.query.filter_by(_post_id=post.id).count()
            collection_amount = Collection.query.filter_by(_post_id=post.id).count()
            temp_post = {'post_id': post.id, 'title': post.title, 'content': post.content, 'comment': [],
                         'like_amount': like_amount, 'collection_amount': collection_amount, 'comment_amount': None}
            comment_list = PostComment.query.filter_by(_post_id=post.id).all()
            count = 0
            for comment in (comment_list or []):
                count += 1
                user = User.query.get(comment.user_id)
                comment_info = {'user_name': user.name, 'content': comment.content}
                temp_post['comment'].append(comment_info)
            temp_post['comment_amount'] = count
            data.append(temp_post)
            amount_count += 1
            if amount is not None:
                if (amount_count == amount):
                    break

    return jsonify(data)


@app.route('/api/post/new-response', methods=['POST'])
@login_required
def new_response():
    post_id = request.values.get('post_id', '')
    like = request.values.get('like', None)
    collection = request.values.get('collection', None)

    if like:
        if like in ['True', 'False']:
            like = istrue(like)
        else:
            abort(400)
    elif collection:
        if collection in ['True', 'False']:
            collection = istrue(collection)
        else:
            abort(400)
    else:
        abort(400)
    try:
        post_id = int(post_id)
    except:
        abort(400)

    data = False
    if like:
        exist = Like.query.filter_by(_post_id=post_id, _user_id=current_user.id).first()
        print(exist == None)
        if exist == None:
            Like.create(post_id=post_id, user_id=current_user.id)
            data = True
    if collection:
        exist = Collection.query.filter_by(_post_id=post_id, _user_id=current_user.id).first()
        print(exist == None)
        if exist == None:
            Collection.create(post_id=post_id, user_id=current_user.id)
            data = True
    return jsonify(data)


@app.route('/api/post/new-comment', methods=['POST'])
@login_required
def new_comment():
    post_id = request.values.get('post_id', '')
    content = request.values.get('content', '')

    try:
        post_id = int(post_id)
    except:
        abort(400)
    if isempty(content):
        abort(400)

    PostComment.create(post_id=post_id, user_id=current_user.id, content=content)
    data = True

    return jsonify(data)

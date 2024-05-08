from recipe_app.models import User


users = User.objects.all()
userid_table = {u.id: u for u in users}
username_table = {u.username: u for u in users}


def authenticate(username, password):
    user = user = username_table.get(username, None)
    if user and password == user.password:
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

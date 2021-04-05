import db

users_settings = (f"{user.id}: {user.lang}, {user.color},{user.size}\n" for user in db.User.objects())
print(*(users_settings))

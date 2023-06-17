from modules import database as db

users = db.fetch_all_users()
usernames = [user['usernames'] for user in users.data]
print(usernames)
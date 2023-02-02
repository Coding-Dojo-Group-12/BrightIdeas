from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, post

class Like:
    db = 'BrightIdeas'
    
    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id
        
    @classmethod    
    def save(cls,data):
        query = 'INSERT INTO likes (user_id, post_id) VALUES (%(user_id)s, %(post_id)s);'
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def count_likes(cls, post_id):
        query = 'SELECT COUNT(*) FROM likes WHERE post_id=%s;'
        data = (post_id,)
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            return result[0]['COUNT(*)']
        else:
            print("Error executing query:", query, data)
            return 0
        
    @classmethod
    def has_liked(cls, user_id, post_id):
        query = 'SELECT * FROM likes WHERE user_id=%(user_id)s, AND post_id=%(post_id)s;'
        data = {
            'user_id' : user_id,
            'post_id' : post_id
        }
        result = connectToMySQL(cls.db).query_db(query, data)
        return len(result) > 0
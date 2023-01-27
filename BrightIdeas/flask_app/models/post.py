from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app.models import user 

class Post: 
    db = 'BrightIdeas'
    
    def __init__(self,data):
        self.id = data['id']
        self.content = data['content']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id = data['user_id']
        self.user = None
        
    @classmethod
    def save(cls,data):
        query = 'INSERT INTO posts (content, user_id) VALUES (%(content)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_All(cls):
        query = "SELECT * FROM posts;"
        results = connectToMySQL(cls.db).query_db(query)
        posts = []
        for row in results:
            posts.append(cls(row))
        return posts
    
    @classmethod
    def get(cls,data):
        query = 'SELECT * FROM posts WHERE id = %(id)s;'
        result = connectToMySQL(cls.db).query_db(query,data)
        return cls(result[0])
            
    @classmethod
    def update(cls,data):
        query = 'UPDATE posts SET content=%(content)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = 'DELETE FROM posts WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def postUser(cls,data):
        query = 'SELECT * FROM posts LEFT JOIN users ON posts.user_id = users.id WHERE posts.id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        allPosts = []
        for row in results:
            post = cls(results[0])
            userData = {
                'id':row['users.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'createdAt':row['users.createdAt'],
                'updatedAt':row['users.updatedAt']
            }
            oneUser = user.User(userData)
            post.user = oneUser
            allPosts.append(post)
        return allPosts
    
    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['content']) < 15:
            flash('Post must be at least 15 characters', 'post')
            is_valid = False
        return is_valid

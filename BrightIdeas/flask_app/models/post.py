from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app.models import user, like 

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
        query = """
        INSERT INTO posts 
        (content, user_id) 
        VALUES (%(content)s, %(user_id)s);
        """
        return connectToMySQL(cls.db).query_db(query,data)
    
    # @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM posts ORDER BY createdAt DESC;"
    #     results = connectToMySQL(cls.db).query_db(query)
    #     posts = []
    #     for row in results:
    #         posts.append(cls(row))
    #     return posts
    
    # @classmethod
    # def get(cls,data):
    #     query = 'SELECT * FROM posts WHERE id = %(id)s;'
    #     result = connectToMySQL(cls.db).query_db(query,data)
    #     return cls(result[0])
    
    @classmethod
    def get_all_posts(cls):
        query = """
        SELECT * FROM posts
        JOIN users
        ON posts.user_id = users.id
        ORDER BY posts.createdAt DESC;
        """
        results = connectToMySQL(cls.db).query_db(query)
        if len(results) == 0:
            return []
        else:
            all_posts = []
            for post_dict in results:
                post_obj = cls(post_dict)
                user_dict = {
                    "id" : post_dict["users.id"],
                    "firstName" : post_dict["firstName"],
                    "lastName" : post_dict["lastName"],
                    "email" : post_dict["email"],
                    "password" : post_dict["password"],
                    "createdAt" : post_dict["users.createdAt"],
                    "updatedAt" : post_dict["users.updatedAt"],
                }
                user_obj = user.User(user_dict)
                post_obj.user =user_obj
                all_posts.append(post_obj)
            return all_posts
    
    @classmethod
    def get_one_post(cls, data):
        query = """
        SELECT * FROM posts
        JOIN users
        ON posts.user_id = users.id
        WHERE posts.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            post_dict = results[0]
            post_obj = cls(post_dict)
            user_dict = {
                    "id" : post_dict["users.id"],
                    "firstName" : post_dict["firstName"],
                    "lastName" : post_dict["lastName"],
                    "email" : post_dict["email"],
                    "password" : post_dict["password"],
                    "createdAt" : post_dict["users.createdAt"],
                    "updatedAt" : post_dict["users.updatedAt"],
            }
            user_obj = user.User(user_dict)
            post_obj.user = user_obj
        return post_obj
            
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
                'firstName':row['firstName'],
                'lastName':row['lastName'],
                'email':row['email'],
                'password':row['password'],
                'createdAt':row['users.createdAt'],
                'updatedAt':row['users.updatedAt']
            }
            oneUser = user.User(userData)
            post.user = oneUser
            allPosts.append(post)
        return allPosts
    
    @classmethod
    def postLike(cls,data):
        query = 'SELECT * FROM likes LEFT JOIN posts ON likes.post_id = posts.id WHERE posts.id = %(id)s;'
        results = connectToMySQL('users').query_db(query,data)
        allLikes = []
        for row in results:
            likeData = {
                'id' : row['likes.id'],
                'user_id' : row['user_id'],
                'post_id' : row['post_id']
            }
            allLikes.append(likeData)
        return allLikes
    
    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['content']) < 15:
            flash('Post must be at least 15 characters', 'post')
            is_valid = False
        return is_valid
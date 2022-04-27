from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User





# -----------------------------------------------------------------------------

class Show:
    db_name = 'shows'

    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posted_by = User.get_by_id(data['user_id'])
        self.likes_count = None
        # can do an empty list and count the length 
        # or plus and minus 1 in the database if set likes column
        # opted to specifically count the rows when Show.count_likes(data) is called
        # by passing in this class method with the tv show's id when loading the view page.
        # seems to be a clean and efficient way of doing it

    @classmethod
    def save(cls,data):
        query = "INSERT INTO shows (title, network, release_date, description, user_id) VALUES (%(title)s,%(network)s,%(release_date)s,%(description)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_shows = []
        if results:
            for row in results:
                # print(row['release_date'])
                all_shows.append( cls(row) )
        return all_shows

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM shows WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE shows SET title=%(title)s, network=%(network)s, release_date=%(release_date)s, description=%(description)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM shows WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    # I looked into avoiding duplicate entries by using various querys like NOT EXISTS, WHERE NOT IN, INSERT INTO SELECT DISTINCT
    # However I came to the conclusion after some testing that MySQL doesn't allow these duplicates on this many to many table so that issue is addressed.
    @classmethod
    def like_show(cls,data): 
        query = "INSERT INTO liked (user_id, show_id) VALUES (%(user_id)s,%(id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def unlike_show(cls,data): 
        query = "DELETE FROM liked WHERE show_id=%(id)s AND user_id=%(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    # here is where I use a join - I could have used a more sophisticated left join 
    # however I opted to keep the code clean and easy to interpret
    @classmethod
    def liked_shows(cls): 
        query = "SELECT * FROM liked JOIN shows WHERE id = show_id;"
        return connectToMySQL(cls.db_name).query_db(query)

    @classmethod
    def count_likes(cls, data):
        query = "SELECT * FROM liked WHERE %(id)s = show_id;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        likes = 0
        if results:
            for row in results:
                likes = likes + 1
        return likes

# Validations-------------------------------------------------------------------

    @staticmethod
    def validate_show(show):
        is_valid = True
        if len(show['title']) < 3:
            is_valid = False
            flash("Title must be at least 3 characters","show")
        if len(show['network']) < 3:
            is_valid = False
            flash("Network must be at least 3 characters","show")
        if len(show['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","show")
        if show['release_date'] == "":
            is_valid = False
            flash("Please enter the release date","show")
        return is_valid

"""Application Models"""
#from typing_extensions import Self

import json
from dotenv import load_dotenv
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()


class User:

    """User Model"""
    def __init__(self):
        id = ""
        name = ""
        email = ""
        password = ""
        token = ""
        return

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def get_con(self):
        """Open a connection and create the users table if it doesn't exist"""
        """Execute a query on the database"""
        """Commit the query and close the database"""
        con = sqlite3.connect('users.db')
        cur = con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS users (name TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL)")

        return con
    
    def close_con(self, con):
        
        con.commit()
        con.close()
        return

    def convert_to_user(self, result):
                
        if not result:
            return
        
        self.id = result[0]
        self.name = result[1]
        self.email = result[2]
        self.password = result[3]

        #print("ID: ", self.id)
        #print("Name: ", self.name)
        #print("Email: ", self.email)
        #print("Pass: ", self.password)

        return self
    

    def create(self, name="", email="", password=""):
        """Create a new user"""
        # Values are already validated prior to user creation.

        existing = self.get_by_email(email)
        if existing:
            return

        # Insert the data into the database        
        con = self.get_con()
        cur = con.cursor()

        cur.execute("INSERT INTO 'users'('name', 'email', 'password') VALUES (?,?,?)", (name, email, self.encrypt_password(password)))

        self.close_con(con)

        # Return the newly added user.
        user = self.get_by_email(email)
        print(user)
        return user

    def login(self, email, password):
        """Login a user"""
       
        # Get user data from the database        
        con = self.get_con()
        cur = con.cursor()

        #print(self.encrypt_password(password))

        result = cur.execute("SELECT rowid, * FROM 'users' WHERE email = ? AND password = ?", (email, self.encrypt_password(password))).fetchone()
        
        self.close_con(con)
        
        user = self.convert_to_user(result)
        #print("User ID: ? NAME: ? EMAIL: ? PASS: ?", (user.id, user.name, user.email, user.password))
        return user


    def get_by_email(self, email):
        """Get a user by email"""
        
        # Find user data from the database        
        con = self.get_con()
        cur = con.cursor()

        result = cur.execute("SELECT rowid, * FROM 'users' WHERE email = ?", (email,)).fetchone()
        print(result)

        self.close_con(con)

        user = self.convert_to_user(result)

        return user


    def encrypt_password(self, password):
        """Encrypt password"""
        # Currently produces different results which cannot be used for authentication.
        return password
        return generate_password_hash(password)

    
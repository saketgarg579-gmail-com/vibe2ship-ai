import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

class DBManager:
    def __init__(self):
        # Replace 'hackathon_user' and 'YOUR_NEW_PASSWORD' with the ones you just created
        user = "gargsaket17_db_user" 
        password = "BD9tYeOzYVcDx4jR" 
        cluster = "cluster0.cqdh5v0.mongodb.net" # Your cluster address
        
        # This is the most stable way to write the URI
        mongo_uri = f"mongodb+srv://{user}:{password}@{cluster}/vibeship_db?retryWrites=true&w=majority"
        
        try:
            self.client = pymongo.MongoClient(mongo_uri)
            # Try to ping the server to see if the password works
            self.client.admin.command('ping') 
            print("[OK] MongoDB Connected Successfully!")
        except Exception as e:
            print(f"[ERROR] MongoDB Connection Failed: {e}")
            
        self.db = self.client["vibeship_db"]



    def save_task(self, email, task):
        """Saves a task or updates it if the summary already exists."""
        # We use a collection per user for better organization
        collection = self.db["user_tasks"]
        
        # Use the summary and email together as a unique ID
        filter_criteria = {"email": email, "summary": task['summary']}
        
        # update_one with upsert=True means: Update if exists, create if not.
        collection.update_one(
            filter_criteria, 
            {"$set": task}, 
            upsert=True
        )

    def get_tasks(self, email):
        """Retrieves all tasks for a specific user."""
        collection = self.db["user_tasks"]
        return list(collection.find({"email": email}))

    def mark_as_called(self, email, summary):
        """Marks a task as 'called' in the database so they aren't spammed."""
        collection = self.db["user_tasks"]
        collection.update_one(
            {"email": email, "summary": summary}, 
            {"$set": {"called": True}}
        )

    def clear_tasks(self, email):
        """Clears all tasks for a user (used during logout or reset)."""
        collection = self.db["user_tasks"]
        collection.delete_many({"email": email})

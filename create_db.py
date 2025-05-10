from app import create_app, mongo

app = create_app()

@app.cli.command('create-db')
def create_db():
    # Example of creating a collection if it doesn't exist
    mongo.db.create_collection('users')  # This is optional
    print("MongoDB collections initialized!")

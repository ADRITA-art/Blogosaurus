from app import create_app
from dotenv import load_dotenv


load_dotenv()


application = create_app()


app = application

if __name__ == "__main__":
    app.run()
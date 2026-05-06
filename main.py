from wikish.cli import app
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

if __name__ == "__main__":
    try:
        app()
    except KeyboardInterrupt:
        print("\nOperation cancelled")
    except Exception as e:
        print(f"Error: {str(e)}")
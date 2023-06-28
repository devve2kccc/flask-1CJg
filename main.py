from website import create_app
import os

# Content of main.py

app = create_app()

if __name__ == '__main__':
    app.run((debug=True, port=os.getenv("PORT", default=5000))

# Import the create_app function from your website package (the folder containing __init__.py)
from website import create_app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Run the Flask development server
    # debug=True allows for auto-reloading when you change code
    app.run(debug=True)
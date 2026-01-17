from flask import Flask, redirect, url_for
from users import users_bp  # Import your blueprint

app = Flask(__name__)

# Register the blueprint (routes start with /citizen)
app.register_blueprint(users_bp, url_prefix='/citizen')

# --- THE FIX IS HERE ---
@app.route('/')
def index():
    # Automatically redirect localhost:5000 -> localhost:5000/citizen/home
    return redirect(url_for('users.home'))

if __name__ == '__main__':
    app.run(debug=True)
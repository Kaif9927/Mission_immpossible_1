from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret_key"  # Replace with a secure key

# Load users from text files
def load_users(file):
    users = {}
    with open(file, "r") as f:
        for line in f:
            username, password = line.strip().split(",")
            users[username] = password
    return users

# Save a new user to the file
def save_user(file, username, password):
    with open(file, "a") as f:
        f.write(f"{username},{password}\n")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users_A = load_users("users_A.txt")
        users_B = load_users("users_B.txt")

        if username in users_A and users_A[username] == password:
            session["user"] = username
            return redirect(url_for("game"))
        elif username in users_B and users_B[username] == password:
            session["pending_user"] = username
            return redirect(url_for("second_login"))
        else:
            return "Invalid username or password. Please try again."

    return render_template("login.html")
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Always save as User A
        user_type = "A"
        
        # Save user data to users_A.txt (or use appropriate file/database)
        with open(f"users_{user_type}.txt", "a") as file:
            file.write(f"{username} {password}\n")
        
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route("/second-login", methods=["GET", "POST"])
def second_login():
    if "pending_user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users_B = load_users("users_B.txt")
        if username in users_B and users_B[username] == password and username != session["pending_user"]:
            return redirect(url_for("hidden_data"))
        else:
            return "Invalid second user or same as the first user."

    return render_template("second_login.html")

@app.route("/game")
def game():
    if "user" in session:
        return render_template("game.html")
    return redirect(url_for("login"))

@app.route("/hidden-data")
def hidden_data():
    if "pending_user" in session:
        return render_template("hidden_data.html")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

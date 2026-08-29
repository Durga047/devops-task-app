from flask import Flask, render_template, request, redirect, url_for
from database.db import get_connection, init_db

app = Flask(__name__)

# Initialize database
init_db()


# -------------------------
# HOME - READ TASKS
# -------------------------
@app.route("/")
def home():

    connection = get_connection()

    tasks = connection.execute(
        "SELECT * FROM tasks ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template("index.html", tasks=tasks)


# -------------------------
# ADD TASK - CREATE
# -------------------------
@app.route("/add", methods=["POST"])
def add_task():

    title = request.form["title"]
    description = request.form["description"]

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO tasks (title, description)
        VALUES (?, ?)
        """,
        (title, description)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("home"))


# -------------------------
# UPDATE TASK - UPDATE
# -------------------------
@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):

    status = request.form["status"]

    connection = get_connection()

    connection.execute(
        """
        UPDATE tasks
        SET status = ?
        WHERE id = ?
        """,
        (status, task_id)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("home"))


# -------------------------
# DELETE TASK - DELETE
# -------------------------
@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):

    connection = get_connection()

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("home"))


# -------------------------
# HEALTH CHECK
# -------------------------
@app.route("/health")
def health():

    return {
        "status": "UP"
    }


# -------------------------
# START APPLICATION
# -------------------------
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

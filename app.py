from flask import Flask, render_template, request, redirect, url_for
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

tasks = []

tasks_created = Counter(
    "todo_tasks_created",
    "Total number of created ToDo tasks"
)

tasks_deleted = Counter(
    "todo_tasks_deleted",
    "Total number of deleted ToDo tasks"
)

tasks_current = Gauge(
    "todo_tasks_current",
    "Current number of ToDo tasks"
)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_text = request.form.get("task")

        if task_text and task_text.strip():
            tasks.append(task_text.strip())
            tasks_created.inc()
            tasks_current.set(len(tasks))

        return redirect(url_for("index"))

    tasks_current.set(len(tasks))
    return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        tasks_deleted.inc()
        tasks_current.set(len(tasks))

    return redirect(url_for("index"))


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
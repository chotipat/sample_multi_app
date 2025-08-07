from flask import Flask, request, render_template
from pymongo import MongoClient
from datetime import datetime, UTC

app = Flask(__name__)
client = MongoClient("mongodb://mongodb:27017/")
db = client["access_logs"]
collection = db["visits"]

@app.route("/")
def index():
    ip = request.remote_addr
    collection.insert_one({
        "ip": ip,
        "timestamp": datetime.now(UTC)
    })
    count = collection.count_documents({"ip": ip})
    return render_template("index.html", ip=ip, count=count)

@app.route("/stats")
def stats():
    ip_counts = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ])
    return render_template("stats.html", stats=ip_counts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

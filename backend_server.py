# minimal backend using flask
from flask import Flask, jsonify
import requests

app = Flask(__name__)

USCF_URL = "https://ratings-api.uschess.org/api/v1/members/31482242/sections?Offset=0&Size=50"

@app.route('/leaderboard')
def leaderboard():
    data = requests.get(USCF_URL).json()
    ratings = [r for section in data["items"] for r in section["ratingRecords"]]
    most_recent = sorted(ratings, key=lambda r: r.get("event", {}).get("date", ""), reverse=True)[0]
    return jsonify({"rating": most_recent["postRating"]})

if __name__ == '__main__':
    app.run(debug=True)

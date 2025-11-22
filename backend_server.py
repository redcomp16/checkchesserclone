from flask import Flask, jsonify
import requests

app = Flask(__name__)

# List of players
players = [
    {"name": "Kirby Lin", "school": "Central", "uscf": 16798007},
    {"name": "Calvin Wang", "school": "Central", "uscf": 30757348},
    {"name": "Edward Lin", "school": "Central", "uscf": 30757702},
    {"name": "Olivia Ryerson", "school": "Masterman", "uscf": 16727082},
    {"name": "Eric Yeung", "school": "Masterman", "uscf": 30868847},
    {"name": "Ali Hawkes", "school": "Masterman", "uscf": 15777743}
]

def fetch_rating(uscf_id):
    url = f"https://ratings-api.uschess.org/api/v1/members/{uscf_id}/sections?Offset=0&Size=50"
    try:
        data = requests.get(url).json()
        ratings = [r for section in data.get("items", []) for r in section.get("ratingRecords", [])]
        if not ratings:
            return None
        # Get most recent rating
        most_recent = sorted(ratings, key=lambda r: r.get("event", {}).get("date", ""), reverse=True)[0]
        return most_recent["postRating"]
    except:
        return None

@app.route("/")
def leaderboard():
    result = []
    for p in players:
        rating = fetch_rating(p["uscf"])
        result.append({
            "name": p["name"],
            "school": p["school"],
            # For sorting, store as int if possible; N/A becomes 0
            "rating": rating if isinstance(rating, int) else 0
        })

    # Sort by descending rating
    result.sort(key=lambda x: x["rating"], reverse=True)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Codeforces API
def fetch_codeforces_data(handle):
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["result"][0]
        return {
            "platform": "Codeforces",
            "handle": handle,
            "rating": data.get("rating", "Unrated"),
            "maxRating": data.get("maxRating", "Unrated"),
            "rank": data.get("rank", "N/A"),
            "maxRank": data.get("maxRank", "N/A")
        }
    else:
        return {"error": "User not found or API error"}

# CodeChef Scraper (no public API)
def fetch_codechef_data(handle):
    url = f"https://www.codechef.com/users/{handle}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "User not found or network error"}

    soup = BeautifulSoup(response.text, "html.parser")
    rating_span = soup.find("div", class_="rating-number")
    stars_span = soup.find("span", class_="rating-star")
    if rating_span:
        return {
            "platform": "CodeChef",
            "handle": handle,
            "rating": rating_span.text.strip(),
            "stars": stars_span.text.strip() if stars_span else "N/A"
        }
    else:
        return {"error": "Could not parse data"}


# ✅ FIXED: AtCoder Scraper
def fetch_atcoder_data(handle):
    url = f"https://atcoder.jp/users/{handle}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "User not found or network error"}

    soup = BeautifulSoup(response.text, "html.parser")
    try:
        tables = soup.find_all("table")
        rating_table = tables[0]
        rows = rating_table.find_all("tr")

        current_rating = rows[1].find_all("td")[0].text.strip()
        highest_rating = rows[2].find_all("td")[0].text.strip()
        rank = rows[0].find_all("td")[0].text.strip()

        return {
            "platform": "AtCoder",
            "handle": handle,
            "rating": current_rating,
            "highestRating": highest_rating,
            "rank": rank
        }
    except Exception as e:
        return {"error": "Could not parse AtCoder data"}


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analyze', methods=["POST"])
def analyze():
    platform = request.form["platform"]
    handle = request.form["handle"].strip()
    
    if platform == "codeforces":
        data = fetch_codeforces_data(handle)
    elif platform == "codechef":
        data = fetch_codechef_data(handle)
    elif platform == "atcoder":
        data = fetch_atcoder_data(handle)
    else:
        data = {"error": "Unsupported platform"}

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

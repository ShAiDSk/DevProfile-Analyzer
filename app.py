from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
from groq import Groq
from bs4 import BeautifulSoup  # <--- NEEDED FOR CODECHEF

# 1. Load environment variables
load_dotenv()

app = Flask(__name__)

# --- 2. SETUP CLIENT (Groq) ---
api_key = os.getenv("GROQ_API_KEY") or os.getenv("GEMINI_API_KEY")

client = None
if api_key:
    try:
        client = Groq(api_key=api_key)
    except Exception as e:
        print(f"❌ Client Setup Error: {e}")
else:
    print("❌ ERROR: API Key not found in .env")


# --- 1. CODEFORCES ---
def get_codeforces_data(handle):
    try:
        user_resp = requests.get(f"https://codeforces.com/api/user.info?handles={handle}").json()
        rating_resp = requests.get(f"https://codeforces.com/api/user.rating?handle={handle}").json()

        if user_resp['status'] != 'OK': return None
        
        user = user_resp['result'][0]
        ratings = rating_resp.get('result', [])

        return {
            'handle': user.get('handle'),
            'rank': user.get('rank', 'unrated'),
            'rating': user.get('rating', 0),
            'maxRating': user.get('maxRating', 0),
            'solved': len(ratings) * 3, # Estimate
            'avatar': user.get('titlePhoto'),
            'ratingHistory': [r['newRating'] for r in ratings],
            'contestHistory': [r['contestName'] for r in ratings]
        }
    except: return None

# --- 2. LEETCODE ---
def get_leetcode_data(handle):
    query = """
    query userPublicProfile($username: String!) {
        matchedUser(username: $username) {
            username
            profile { userAvatar realName ranking }
            submitStats {
                acSubmissionNum { difficulty count }
            }
        }
        userContestRanking(username: $username) {
            rating
            topPercentage
        }
    }
    """
    try:
        resp = requests.post('https://leetcode.com/graphql', 
                             json={'query': query, 'variables': {'username': handle}},
                             headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}).json()
        
        if 'errors' in resp or not resp.get('data') or not resp['data']['matchedUser']: 
            return None
        
        user = resp['data']['matchedUser']
        contest = resp['data']['userContestRanking']
        
        current_rating = int(contest['rating']) if contest else 0
        top_percentage = f"Top {contest['topPercentage']}%" if contest else "Unrated"

        total_solved = 0
        for stat in user['submitStats']['acSubmissionNum']:
            if stat['difficulty'] == 'All':
                total_solved = stat['count']

        return {
            'handle': user['username'],
            'rank': top_percentage,
            'rating': current_rating,
            'maxRating': "N/A", 
            'solved': total_solved,
            'avatar': user['profile']['userAvatar'],
            'ratingHistory': [x['count'] for x in user['submitStats']['acSubmissionNum'] if x['difficulty'] != 'All'],
            'contestHistory': ['Easy', 'Medium', 'Hard'] 
        }
    except Exception as e:
        print(f"LeetCode Error: {e}") 
        return None

# --- 3. ATCODER ---
def get_atcoder_data(handle):
    try:
        history = requests.get(f"https://atcoder.jp/users/{handle}/history/json").json()
        if not history: return None

        latest = history[-1]
        max_rating = max([x['NewRating'] for x in history])
        
        return {
            'handle': handle,
            'rank': get_atcoder_rank_color(latest['NewRating']),
            'rating': latest['NewRating'],
            'maxRating': max_rating,
            'solved': len(history) * 4, # Estimate
            'avatar': "https://img.atcoder.jp/assets/atcoder.png",
            'ratingHistory': [x['NewRating'] for x in history],
            'contestHistory': [x['ContestName'] for x in history]
        }
    except: return None

def get_atcoder_rank_color(rating):
    if rating < 400: return "Gray"
    if rating < 800: return "Brown"
    if rating < 1200: return "Green"
    if rating < 1600: return "Cyan"
    if rating < 2000: return "Blue"
    if rating < 2400: return "Yellow"
    if rating < 2800: return "Orange"
    return "Red"

# --- 4. GITHUB ---
def get_github_data(handle):
    try:
        user_url = f"https://api.github.com/users/{handle}"
        user_resp = requests.get(user_url)
        repos_url = f"https://api.github.com/users/{handle}/repos?sort=updated&per_page=100"
        repos_resp = requests.get(repos_url)

        if user_resp.status_code != 200: return None
        
        user = user_resp.json()
        repos = repos_resp.json()

        total_stars = sum([repo['stargazers_count'] for repo in repos])
        languages = {}
        for repo in repos:
            lang = repo['language']
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
        
        top_langs = dict(sorted(languages.items(), key=lambda item: item[1], reverse=True)[:5])

        badges = []
        if user['followers'] > 100: badges.append("🔥 Famous")
        if total_stars > 50: badges.append("⭐ Star Hunter")
        if len(repos) > 50: badges.append("🚜 Code Machine")
        if 'Python' in top_langs: badges.append("🐍 Pythonista")
        if 'JavaScript' in top_langs: badges.append("⚡ JS Wizard")

        return {
            'handle': user['login'],
            'rank': f"{user['followers']} Followers",
            'rating': total_stars, 
            'maxRating': user['public_repos'],
            'solved': user['public_repos'], 
            'avatar': user['avatar_url'],
            'badges': badges,
            'languages': top_langs,
            'ratingHistory': [r['stargazers_count'] for r in repos[:10]], 
            'contestHistory': [r['name'] for r in repos[:10]]
        }
    except Exception as e:
        print(e)
        return None

# --- 5. CODECHEF (New & Fixed) ---
def get_codechef_data(handle):
    try:
        url = f"https://www.codechef.com/users/{handle}"
        # CodeChef requires strict headers or it blocks the request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        page = requests.get(url, headers=headers)
        if page.status_code != 200: return None
        
        soup = BeautifulSoup(page.content, 'html.parser')

        # Find Rating
        rating_div = soup.find('div', class_='rating-number')
        if not rating_div: return None
        current_rating = int(rating_div.text.strip())

        # Find Max Rating
        max_rating_div = soup.find('small')
        max_rating = current_rating
        if max_rating_div and 'Highest Rating' in max_rating_div.text:
            # Extract number from text like "(Highest Rating 1234)"
            txt = max_rating_div.text
            import re
            nums = re.findall(r'\d+', txt)
            if nums: max_rating = int(nums[0])

        # Find Stars/Rank
        stars = soup.find('span', class_='rating')
        rank = stars.text.strip() if stars else "Unrated"

        # Find Avatar
        avatar_img = soup.find('div', class_='user-details-container').find('img')
        avatar = avatar_img['src'] if avatar_img else "https://cdn.codechef.com/sites/all/themes/abacus/assets/img/codechef-logo.png"
        if avatar.startswith("/"): avatar = "https://codechef.com" + avatar

        return {
            'handle': handle,
            'rank': rank,
            'rating': current_rating,
            'maxRating': max_rating,
            'solved': "N/A", # Hard to scrape dynamically
            'avatar': avatar,
            'ratingHistory': [current_rating, current_rating], 
            'contestHistory': ['Current', 'Current']
        }
    except Exception as e: 
        print(f"CodeChef Error: {e}")
        return None


# --- 6. PERSONA ENGINE ---
def generate_persona(data):
    try: r_val = float(data.get('rating', 0))
    except: r_val = 0
    
    try: m_val = float(data.get('maxRating', 0)) if data.get('maxRating') != "N/A" else 0
    except: m_val = 0

    rating_score = min(r_val / 30, 60) 
    repo_score = min(m_val * 2, 30)
    
    power_level = int(rating_score + repo_score + 10)
    if power_level > 100: power_level = 100
    
    title = "Code Novice 🌱"
    description = "Just starting the journey. Potential is high!"
    
    if power_level > 90:
        title = "Grandmaster 🧙‍♂️"
        description = "Your code compiles on the first try. You dream in binary."
    elif power_level > 75:
        title = "System Architect 🏗️"
        description = "Building digital empires one commit at a time."
    elif power_level > 50:
        title = "Bug Hunter 🐞"
        description = "You crush errors before breakfast. Efficiency is your middle name."
    
    if "Python" in str(data): title += " (The Snake Charmer)"
    
    return { 'title': title, 'level': power_level, 'description': description }


# --- 7. AI FUNCTION ---
def get_ai_feedback(stats, mode="roast"):
    if not client:
        return "AI Error: API Key missing."

    try:
        prompt_text = f"""
        Act as a senior developer reviewing a junior's profile.
        Stats: {stats}
        
        Task: Write a short, funny, 2-sentence {mode} of this profile. 
        Plain text only. No markdown.
        """

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        return completion.choices[0].message.content

    except Exception as e:
        print(f"❌ GROQ ERROR: {e}")
        return f"AI Error: {str(e)}"


# --- ROUTES ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    platform = data.get('platform')
    handle = data.get('handle')
    
    profile_data = None
    
    if platform == 'Codeforces': profile_data = get_codeforces_data(handle)
    elif platform == 'LeetCode': profile_data = get_leetcode_data(handle)
    elif platform == 'AtCoder': profile_data = get_atcoder_data(handle)
    elif platform == 'GitHub': profile_data = get_github_data(handle)
    elif platform == 'CodeChef': profile_data = get_codechef_data(handle) # <--- ADDED THIS LINE
    
    if profile_data:
        profile_data['persona'] = generate_persona(profile_data)
        return jsonify({'success': True, 'data': profile_data})
    else:
        return jsonify({'success': False, 'message': f'User not found or API error on {platform}'})

@app.route('/ask-ai', methods=['POST'])
def ask_ai():
    data = request.json
    mode = data.get('mode') # 'roast' or 'hype'
    stats = data.get('stats')
    
    feedback = get_ai_feedback(stats, mode)
    return jsonify({'success': True, 'message': feedback})    


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
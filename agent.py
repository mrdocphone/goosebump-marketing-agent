import os
import requests
from google import genai

# This loads our secure key from GitHub automatically
client = genai.Client()

def get_viral_trend():
    """Scrapes a random high-value community to find a problem trend."""
    import random # Imports the ability to choose randomly
    
    # Master list of your target niche communities
    target_urls = [
        "https://www.reddit.com/r/SaaS/hot.json?limit=3",
        "https://www.reddit.com/r/GrowthHacking/hot.json?limit=3",
        "https://www.reddit.com/r/startups/hot.json?limit=3",
        "https://www.reddit.com/r/ArtificialInteligence/hot.json?limit=3",
        "https://www.reddit.com/r/marketing/hot.json?limit=3"
    ]
    
    # The agent picks a different community from the list every time it runs
    url = random.choice(target_urls)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        res = requests.get(url, headers=headers).json()
        # We grab the second post [1] to skip pinned moderator announcements
        top_post = res['data']['children'][1]['data']
        return {"title": top_post['title'], "text": top_post['selftext'][:1500]}
    except Exception as e:
        print(f"Forced Fallback activated due to rate limits: {e}")
        return {
            "title": "Scaling AI Workflows in 2026", 
            "text": "Users looking for high-performance, automated pipeline optimizations."
        }

def build_marketing_page(title, context):
    """Sends the trend data to Gemini to design a conversion-optimized web engine page."""
    prompt = f"""
    You are an elite conversion rate optimization (CRO) marketing engineer.
    A major trend/problem is occurring across the web right now: "{title}"
    Contextual background: {context}
    
    Task: Build a single-page production ready HTML layout using clean Tailwind CSS via CDN.
    The layout must feature:
    1. An urgent, high-impact hero section addressing this problem directly.
    2. A structured, easy-to-read explanation or resolution guide.
    3. An incredibly clean, persuasive call-to-action (CTA) section pointing users toward an affiliate link, consulting booking, or product offer.
    
    IMPORTANT: Return ONLY the raw valid HTML code. Do not wrap the code blocks in markdown fences like ```html or add chat introductions. Just give me the code starting with <!DOCTYPE html>.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text

def main():
    print("Agent Core online. Fetching global trend metrics...")
    trend = get_viral_trend()
    print(f"Target locked onto trend: {trend['title']}")
    
    print("Sending blueprint to Gemini Core for processing...")
    html_content = build_marketing_page(trend['title'], trend['text'])
    
    # Strip any stray markdown syntax if the model accidentally returns it
    clean_html = html_content.replace("```html", "").replace("```", "").strip()
    
    # Write the asset directly to our working folder
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(clean_html)
    print("Success. Production-ready index.html asset built.")
    
    # --- CRITICAL FIX START ---
    # Create an empty .nojekyll file to stop GitHub Pages from using Jekyll and crashing
    with open(".nojekyll", "w", encoding="utf-8") as f:
        f.write("")
    print("Bypass flag created: .nojekyll file successfully added.")
    # --- CRITICAL FIX END ---

if __name__ == "__main__":
    main()

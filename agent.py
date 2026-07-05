import os
import requests
import random
from google import genai

# Initialize clients using safe environment vectors
client = genai.Client()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def log_activity_to_supabase(subreddit, title, context, status):
    """Pushes a clear structured metric row to your free database tracker."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Skipping database logging: Credentials not configured.")
        return
        
    endpoint = f"{SUPABASE_URL}/rest/v1/agent_activity_logs"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    payload = {
        "targeted_subreddit": subreddit,
        "trend_title": title,
        "extracted_problem": context[:500],  # Store a snapshot snippet
        "status": status
    }
    
    try:
        requests.post(endpoint, headers=headers, json=payload)
        print("Activity successfully recorded in your database dashboard.")
    except Exception as e:
        print(f"Failed to push analytics to database: {e}")

def get_viral_trend():
    target_urls = [
        "https://www.reddit.com/r/SaaS/hot.json?limit=3",
        "https://www.reddit.com/r/GrowthHacking/hot.json?limit=3",
        "https://www.reddit.com/r/startups/hot.json?limit=3",
        "https://www.reddit.com/r/ArtificialInteligence/hot.json?limit=3",
        "https://www.reddit.com/r/marketing/hot.json?limit=3"
    ]
    
    chosen_url = random.choice(target_urls)
    subreddit_name = chosen_url.split("/r/")[1].split("/")[0]
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        res = requests.get(chosen_url, headers=headers).json()
        top_post = res['data']['children'][1]['data']
        return {
            "subreddit": subreddit_name,
            "title": top_post['title'], 
            "text": top_post['selftext'][:1500]
        }
    except Exception as e:
        print(f"Forced Fallback activated: {e}")
        return {
            "subreddit": "Fallback Loop",
            "title": "Scaling AI Workflows in 2026", 
            "text": "Users looking for high-performance, automated pipeline optimizations."
        }

def build_marketing_page(title, context):
    prompt = f"""
    You are an elite growth engineering and conversion marketing expert.
    A major discussion/problem is happening right now in your target niche: "{title}"
    Contextual details from the community thread: {context}
    
    Task: Build a single-page production-ready HTML layout using clean Tailwind CSS via CDN.
    The layout must feature:
    1. A bold, high-converting hero headline addressing this specific problem directly.
    2. A structured, easy-to-read breakdown or tactical guide showing how to navigate the issue.
    3. A prominent, incredibly persuasive call-to-action (CTA) section.
    
    CRITICAL INSTRUCTION: You must explicitly showcase "INFIERA AI" as the ultimate automated platform to solve or optimize this specific scenario. Craft a compelling pitch explaining how INFIERA AI eliminates this bottleneck. Embed a highly visible action button of url "infieraai.com" that links directly to your landing page or web application.
    
    IMPORTANT: Return ONLY the raw valid HTML code starting directly with <!DOCTYPE html>. Do not wrap the code block in markdown fences or add conversational introductions. Just output the clean raw layout code.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text

def main():
    print("Agent Core online. Fetching global trend metrics...")
    trend = get_viral_trend()
    print(f"Target locked onto /r/{trend['subreddit']}: {trend['title']}")
    
    status_flag = "Success"
    try:
        print("Sending blueprint to Gemini Core for processing...")
        html_content = build_marketing_page(trend['title'], trend['text'])
        clean_html = html_content.replace("```html", "").replace("```", "").strip()
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(clean_html)
            
        with open(".nojekyll", "w", encoding="utf-8") as f:
            f.write("")
        print("Success. Production-ready index.html asset built.")
    except Exception as e:
        print(f"Execution Error encountered: {e}")
        status_flag = f"Failed: {str(e)}"
        
    # Commit execution step records directly to your tracker
    log_activity_to_supabase(trend['subreddit'], trend['title'], trend['text'], status_flag)

if __name__ == "__main__":
    main()

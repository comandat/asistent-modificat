import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def google_search(query, num_results=5):
    """
    Perform a Google search (using a free scraping method or API if configured).
    This is a simplified implementation using basic requests for demonstration.
    For production, use Brave Search API or Google Custom Search API.
    """
    print(f"🔍 Searching for: {query}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    url = f"https://www.google.com/search?q={query}&num={num_results}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        for g in soup.find_all('div', class_='g'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title = g.find('h3').text if g.find('h3') else link
                snippet = g.find('div', class_='VwiC3b').text if g.find('div', class_='VwiC3b') else ""
                results.append({'title': title, 'link': link, 'snippet': snippet})
        return results
    except Exception as e:
        print(f"❌ Search error: {e}")
        return []

def extract_content(url):
    """
    Fetch and extract main content from a URL using readability logic.
    """
    print(f"📄 Reading: {url}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove scripts and styles
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.extract()
            
        text = soup.get_text(separator='\n')
        # Simple cleanup
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text[:5000] # Return first 5000 chars to save tokens
    except Exception as e:
        return f"Error reading {url}: {e}"

def deep_research(topic, depth=3):
    """
    Perform deep research on a topic.
    1. Search query.
    2. Visit top 3 links.
    3. Extract content.
    4. Compile report.
    """
    print(f"🚀 Starting Deep Research on: {topic}")
    
    # Step 1: Search
    results = google_search(topic, num_results=depth)
    
    if not results:
        print("❌ No results found.")
        return

    report = f"# Research Report: {topic}\n\n"
    
    # Step 2 & 3: Visit & Extract
    for i, res in enumerate(results):
        print(f"[{i+1}/{len(results)}] Analyzing: {res['title']}")
        content = extract_content(res['link'])
        
        report += f"## Source {i+1}: {res['title']}\n"
        report += f"**URL:** {res['link']}\n"
        report += f"**Snippet:** {res['snippet']}\n"
        report += f"**Key Content:**\n{content[:1000]}...\n\n" # Summarize first 1k chars
        
    # Step 4: Output Report
    filename = f"research_{topic.replace(' ', '_')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"✅ Research complete. Report saved to: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nanobot Deep Research Tool")
    parser.add_argument("topic", help="Topic to research")
    parser.add_argument("--depth", type=int, default=3, help="Number of sources to analyze")
    args = parser.parse_args()
    
    deep_research(args.topic, args.depth)

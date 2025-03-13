import requests
import time
import os
import webbrowser
from tkinter import Tk, Label, Button, Text, Scrollbar, messagebox, filedialog, StringVar, OptionMenu
from plyer import notification

# API Keys and URLs
NEWS_API_KEY = "8c4cf72a3bfa4280b6b5e0e683792225"
NEWSDATA_API_KEY = "pub_74313ef1904cc18aeca4dc1aad9228697f8a5"

NEWS_API_URLS = {
    "Business Headlines (US)": "https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=" + NEWS_API_KEY,
    "TechCrunch Headlines": "https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=" + NEWS_API_KEY,
    "Wall Street Journal": "https://newsapi.org/v2/everything?domains=wsj.com&apiKey=" + NEWS_API_KEY,
    "Tesla Articles": "https://newsapi.org/v2/everything?q=tesla&sortBy=publishedAt&apiKey=" + NEWS_API_KEY,
    "Apple Articles": "https://newsapi.org/v2/everything?q=apple&sortBy=popularity&apiKey=" + NEWS_API_KEY,
}

NEWSDATA_API_URL = f"https://newsdata.io/api/1/latest?apikey={NEWSDATA_API_KEY}&category=politics&country=bd"

# Fetch news data from NewsAPI
def fetch_news_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["status"] == "ok":
            return data["articles"]
        else:
            print("Failed to fetch news:", data.get("message", "Unknown error"))
            return []
    except Exception as e:
        print("Error fetching news:", e)
        return []

# Fetch news data from NewsData.io
def fetch_newsdata():
    try:
        response = requests.get(NEWSDATA_API_URL)
        response.raise_for_status()
        data = response.json()
        if data["status"] == "success":
            return data["results"]
        else:
            print("Failed to fetch news:", data.get("message", "Unknown error"))
            return []
    except Exception as e:
        print("Error fetching news:", e)
        return []

# Step-by-step reveal in CLI
def reveal_news_cli(article):
    os.system("cls" if os.name == "nt" else "clear")  # Clear terminal
    print("Breaking News Alert! Something big is happening...\n")
    time.sleep(2)

    print(f"Breaking News: {article.get('title', 'No title available')}\n")
    time.sleep(2)

    summary = article.get("description") or article.get("content", "No summary available.")
    print(f"Summary: {summary.split('. ')[0]}\n")
    time.sleep(2)

    if len(summary.split(". ")) > 1:
        print(f"Summary Contd.: {summary.split('. ')[1]}\n")
        time.sleep(2)

    print(f"Key Detail: {article.get('content', 'No additional details available.')}\n")
    time.sleep(2)

    print(f"Read more: {article.get('url', 'No URL available')}\n")
    time.sleep(1)

    save_option = input("Do you want to save this article? (yes/no): ").strip().lower()
    if save_option == "yes":
        save_article(article)

    if article.get("url"):
        webbrowser.open(article["url"])  # Open article in browser

# Save article to a file
def save_article(article):
    try:
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filename:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Title: {article.get('title', 'No title')}\n")
                file.write(f"Summary: {article.get('description', 'No summary')}\n")
                file.write(f"Content: {article.get('content', 'No content')}\n")
                file.write(f"URL: {article.get('url', 'No URL')}\n")
            print(f"Article saved to {filename}")
    except Exception as e:
        print("Error saving article:", e)

# GUI Implementation
class NewsScavengerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("The News Scavenger")
        self.articles = []
        self.current_article_index = 0

        # GUI Layout
        self.title_label = Label(root, text="The News Scavenger", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        self.source_var = StringVar(root)
        self.source_var.set("Business Headlines (US)")  # Default source
        self.source_menu = OptionMenu(root, self.source_var, *NEWS_API_URLS.keys(), "Politics Headlines (BD)")
        self.source_menu.pack(pady=10)

        self.fetch_button = Button(root, text="Fetch News", command=self.fetch_news)
        self.fetch_button.pack(pady=5)

        self.news_text = Text(root, wrap="word", height=15, width=60)
        self.news_text.pack(pady=10)

        self.scrollbar = Scrollbar(root, command=self.news_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.news_text.config(yscrollcommand=self.scrollbar.set)

        self.next_button = Button(root, text="Next", command=self.next_stage)
        self.next_button.pack(pady=5)

        self.read_more_button = Button(root, text="Read More", command=self.read_more)
        self.read_more_button.pack(pady=5)

        self.save_button = Button(root, text="Save", command=self.save_article)
        self.save_button.pack(pady=5)

        self.skip_button = Button(root, text="Skip", command=self.skip_article)
        self.skip_button.pack(pady=5)

    def fetch_news(self):
        source = self.source_var.get()
        if source == "Politics Headlines (BD)":
            self.articles = fetch_newsdata()
        else:
            self.articles = fetch_news_api(NEWS_API_URLS[source])
        self.current_article_index = 0
        self.update_news()

    def update_news(self):
        if self.current_article_index < len(self.articles):
            article = self.articles[self.current_article_index]
            self.news_text.delete(1.0, "end")
            self.news_text.insert("end", f"Breaking News: {article.get('title', 'No title available')}\n\n")
            self.news_text.insert("end", f"Summary: {article.get('description', 'No summary available.')}\n\n")
            self.news_text.insert("end", f"Key Detail: {article.get('content', 'No additional details available.')}\n\n")
            self.news_text.insert("end", f"Read more: {article.get('url', 'No URL available')}\n")
        else:
            self.news_text.delete(1.0, "end")
            self.news_text.insert("end", "No more news articles available.")

    def next_stage(self):
        self.current_article_index += 1
        self.update_news()

    def read_more(self):
        if self.current_article_index < len(self.articles):
            url = self.articles[self.current_article_index].get("url")
            if url:
                webbrowser.open(url)

    def save_article(self):
        if self.current_article_index < len(self.articles):
            save_article(self.articles[self.current_article_index])

    def skip_article(self):
        self.current_article_index += 1
        self.update_news()

# Main function
def main():
    print("Welcome to The News Scavenger!")
    print("Choose an option:")
    print("1. Use the Command Line Interface (CLI)")
    print("2. Use the Graphical User Interface (GUI)")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        print("Available Sources:")
        for index, source in enumerate(NEWS_API_URLS.keys(), start=1):
            print(f"{index}. {source}")
        print(f"{len(NEWS_API_URLS) + 1}. Politics Headlines (BD)")
        source_choice = input("Enter your choice (1/2/3/4/5/6): ").strip()

        if source_choice.isdigit():
            source_choice = int(source_choice)
            if 1 <= source_choice <= len(NEWS_API_URLS):
                source = list(NEWS_API_URLS.keys())[source_choice - 1]
                articles = fetch_news_api(NEWS_API_URLS[source])
            elif source_choice == len(NEWS_API_URLS) + 1:
                articles = fetch_newsdata()
            else:
                print("Invalid choice. Exiting.")
                return
        else:
            print("Invalid choice. Exiting.")
            return

        for article in articles:
            reveal_news_cli(article)
            proceed = input("Press Enter to continue or 'q' to quit: ").strip().lower()
            if proceed == "q":
                break
    elif choice == "2":
        root = Tk()
        app = NewsScavengerGUI(root)
        root.mainloop()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
import requests
import time
import os
import webbrowser
from tkinter import Tk, Label, Button, Text, Scrollbar, messagebox, filedialog, StringVar, OptionMenu, Entry
from plyer import notification

# ESPN API Endpoints
ESPN_API_BASE = "https://site.api.espn.com/apis/site/v2/sports"
SPORTS = {
    "Football (NFL)": "football/nfl",
    "Basketball (NBA)": "basketball/nba",
    "Baseball (MLB)": "baseball/mlb",
    "Soccer (Premier League)": "soccer/eng.1",
    "Tennis": "tennis"
}

# Fetch live scores
def fetch_live_scores(sport):
    url = f"{ESPN_API_BASE}/{sport}/scoreboard"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("events", [])
    except Exception as e:
        print("Error fetching live scores:", e)
        return []

# Fetch sports news
def fetch_sports_news(sport):
    url = f"{ESPN_API_BASE}/{sport}/news"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("articles", [])
    except Exception as e:
        print("Error fetching sports news:", e)
        return []

# Fetch team standings
def fetch_standings(sport):
    url = f"{ESPN_API_BASE}/{sport}/standings"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("children", [])
    except Exception as e:
        print("Error fetching standings:", e)
        return []

# Step-by-step reveal in CLI
def reveal_news_cli(article):
    os.system("cls" if os.name == "nt" else "clear")  # Clear terminal
    print("Sports Breaking News Alert! Something big is happening...\n")
    time.sleep(2)

    print(f"Headline: {article.get('headline', 'No headline available')}\n")
    time.sleep(2)

    summary = article.get("description", "No summary available.")
    print(f"Summary: {summary.split('. ')[0]}\n")
    time.sleep(2)

    if len(summary.split(". ")) > 1:
        print(f"Summary Contd.: {summary.split('. ')[1]}\n")
        time.sleep(2)

    print(f"Key Detail: {article.get('content', 'No additional details available.')}\n")
    time.sleep(2)

    print(f"Read more: {article.get('links', {}).get('web', {}).get('href', 'No URL available')}\n")
    time.sleep(1)

    save_option = input("Do you want to save this article? (yes/no): ").strip().lower()
    if save_option == "yes":
        save_article(article)

    url = article.get("links", {}).get("web", {}).get("href")
    if url:
        webbrowser.open(url)  # Open article in browser

# Save article to a file
def save_article(article):
    try:
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filename:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Headline: {article.get('headline', 'No headline')}\n")
                file.write(f"Summary: {article.get('description', 'No summary')}\n")
                file.write(f"Content: {article.get('content', 'No content')}\n")
                file.write(f"URL: {article.get('links', {}).get('web', {}).get('href', 'No URL')}\n")
            print(f"Article saved to {filename}")
    except Exception as e:
        print("Error saving article:", e)

# GUI Implementation
class SportsPulseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("The Sports Pulse")
        self.sport_var = StringVar(root)
        self.sport_var.set("Football (NFL)")  # Default sport
        self.articles = []
        self.current_article_index = 0

        # GUI Layout
        self.title_label = Label(root, text="The Sports Pulse", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        self.sport_menu = OptionMenu(root, self.sport_var, *SPORTS.keys())
        self.sport_menu.pack(pady=10)

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
        sport = SPORTS[self.sport_var.get()]
        self.articles = fetch_sports_news(sport)
        self.current_article_index = 0
        self.update_news()

    def update_news(self):
        if self.current_article_index < len(self.articles):
            article = self.articles[self.current_article_index]
            self.news_text.delete(1.0, "end")
            self.news_text.insert("end", f"Headline: {article.get('headline', 'No headline available')}\n\n")
            self.news_text.insert("end", f"Summary: {article.get('description', 'No summary available.')}\n\n")
            self.news_text.insert("end", f"Key Detail: {article.get('content', 'No additional details available.')}\n\n")
            self.news_text.insert("end", f"Read more: {article.get('links', {}).get('web', {}).get('href', 'No URL available')}\n")
        else:
            self.news_text.delete(1.0, "end")
            self.news_text.insert("end", "No more news articles available.")

    def next_stage(self):
        self.current_article_index += 1
        self.update_news()

    def read_more(self):
        if self.current_article_index < len(self.articles):
            url = self.articles[self.current_article_index].get("links", {}).get("web", {}).get("href")
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
    print("Welcome to The Sports Pulse!")
    print("Choose an option:")
    print("1. Use the Command Line Interface (CLI)")
    print("2. Use the Graphical User Interface (GUI)")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        print("Available Sports:")
        for index, sport in enumerate(SPORTS.keys(), start=1):
            print(f"{index}. {sport}")
        sport_choice = input("Enter your choice (1/2/3/4/5): ").strip()

        if sport_choice.isdigit():
            sport_choice = int(sport_choice)
            if 1 <= sport_choice <= len(SPORTS):
                sport = list(SPORTS.values())[sport_choice - 1]
                articles = fetch_sports_news(sport)
                for article in articles:
                    reveal_news_cli(article)
                    proceed = input("Press Enter to continue or 'q' to quit: ").strip().lower()
                    if proceed == "q":
                        break
            else:
                print("Invalid choice. Exiting.")
                return
        else:
            print("Invalid choice. Exiting.")
            return
    elif choice == "2":
        root = Tk()
        app = SportsPulseGUI(root)
        root.mainloop()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
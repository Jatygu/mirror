import json
import os
import sys
import datetime
import random
import re
from collections import Counter, defaultdict

# Optional: for colorful terminal output
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.columns import Columns
    from rich.prompt import Prompt
    from rich.text import Text
    from rich import box
except ImportError:
    print("Missing rich module. Run 'pip install rich' for best visual experience.")
    sys.exit(1)

console = Console()
json_file_path = "C:/Users/device/conversations.json"
search_term_global = None  # For highlighting within selected chats

def load_data(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            data.reverse()
            return data
    except Exception as e:
        console.print(f"[red]Error loading JSON file: {e}[/red]")
        sys.exit(1)

def keyword_analysis(titles, top_n=10):
    words = []
    for title in titles:
        words += title.lower().split()
    return Counter(words).most_common(top_n)

def detect_repetition(titles):
    count = Counter(titles)
    return [title for title, freq in count.items() if freq > 1]

def suggest_rediscovery(titles):
    return random.sample(titles, min(3, len(titles)))

def categorize_titles(titles):
    categories = defaultdict(list)
    for i, title in enumerate(titles):
        t = title.lower()
        if "music" in t or "song" in t or "isrc" in t:
            categories["Music & Licensing"].append((i, title))
        elif "job" in t or "resume" in t or "application" in t:
            categories["Career & Jobs"].append((i, title))
        elif "ai" in t or "script" in t or "automation" in t:
            categories["Automation & AI"].append((i, title))
        elif "gratitude" in t or "appreciation" in t or "affirmation" in t:
            categories["Inner Alignment"].append((i, title))
        elif "art" in t or "image" in t or "creative" in t:
            categories["Creative Flow"].append((i, title))
        else:
            categories["Other"].append((i, title))
    return dict(sorted(categories.items(), key=lambda item: len(item[1]), reverse=True))

def view_chat_by_index(data, index):
    global search_term_global
    if 0 <= index < len(data):
        mapping = data[index].get("mapping", {})
        nodes = sorted(mapping.items(), key=lambda x: x[1].get("create_time", 0))
        console.rule(f"[bold green]Title: {data[index].get('title', 'No Title')}[/bold green]", style="green")
        for _, node_data in nodes:
            message_data = node_data.get("message")
            if message_data:
                role = message_data.get("author", {}).get("role", "unknown")
                parts = message_data.get("content", {}).get("parts", ["No content available"])
                cleaned_parts = [str(p) for p in parts if isinstance(p, (str, dict))]
                text = " ".join(cleaned_parts)
                rich_text = Text(text)
                if search_term_global:
                    rich_text.highlight_words([search_term_global], style="bold bright_green", case_sensitive=False)
                style = "blue" if role == "assistant" else "yellow"
                console.print(Panel.fit(rich_text, title=role.capitalize(), border_style=style, box=box.ROUNDED))

def handle_view_choice(data, titles):
    num = Prompt.ask("Enter the number of the conversation to view").strip()
    if num.isdigit():
        idx = len(data) - int(num)
        view_chat_by_index(data, idx)

def enhanced_search(data):
    global search_term_global
    query = Prompt.ask("Enter a keyword, name, or phrase to search").strip().lower()
    if not query:
        console.print("[dim]No input detected. Returning to menu.[/dim]")
        return

    search_term_global = query
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    results = []

    for i, chat in enumerate(data):
        title = chat.get("title", "")
        mapping = chat.get("mapping", {})
        found = False

        if pattern.search(title):
            found = True
        else:
            for node in mapping.values():
                message_data = node.get("message")
                if not message_data:
                    continue
                content = message_data.get("content", {}).get("parts", [])
                for part in content:
                    if isinstance(part, str) and pattern.search(part):
                        found = True
                        break
                if found:
                    break

        if found:
            results.append((len(data) - i, title))

    if not results:
        console.print("[red]No matches found. Try different or simpler terms.[/red]")
        return

    console.print(f"[green]Found {len(results)} matches:[/green]")
    for number, title in results:
        console.print(f"{number}. {title}")
    handle_view_choice(data, [r[1] for r in results])

if __name__ == "__main__":
    data = load_data(json_file_path)
    titles = [c.get("title", "No Title") for c in data]
    categories = categorize_titles(titles)
    keywords = keyword_analysis(titles, top_n=6)
    repetitions = detect_repetition(titles)
    rediscover = suggest_rediscovery(titles)
    today_date = datetime.datetime.now().strftime("%A, %B %d, %Y")

    # Ensuring proper layout by splitting the tiles into 2 rows
    upper_tiles = [
        Panel(f"[bold yellow]{len(data)}[/bold yellow] total (imported) conversations as of [italic]{today_date}[/italic]", title="🧾 Archive Size", style="yellow", box=box.ROUNDED),
        Panel("\n".join([f"[bold]{w}[/bold]: {f}" for w, f in keywords]), title="📊 Top Keywords", style="blue", box=box.ROUNDED),
        Panel("\n".join([f"[bold]{k}[/bold]: {len(v)}" for k, v in categories.items()]), title="📂 TOP TOPICS", style="black", box=box.ROUNDED)
    ]

    lower_tiles = [
        Panel("\n".join(["Music Rights", "Resume Tailoring", "Job Apps", "Gratitude Routines", "Python Scripts"]), title="🧠 Themes", style="cyan", box=box.ROUNDED),
        Panel("\n".join(repetitions[:5]) if repetitions else "No repeated titles detected.", title="🔁 Repetition Detection", style="green", box=box.ROUNDED),
        Panel("\n".join(rediscover), title="🎁 Joy of Rediscovery", style="bright_magenta", box=box.ROUNDED)
    ]

    console.print(Panel("[bold cyan]Welcome to Chat Insight Life Mirror[/bold cyan]\nYour personal wisdom miner, creative map, and self-reflection engine.", style="bold white on black", box=box.ROUNDED))
    console.print(Columns(upper_tiles, equal=True, expand=True, align="center"))
    console.print(Columns(lower_tiles, equal=True, expand=True, align="center"))

    while True:
        console.print("\n[bold green]How would you like to proceed today?[/bold green]")
        console.print("Type 0 (Legacy), 1 (Browse), 2 (View), 3 (Reflect), 4 (Search), 5 (Random Chat), or 6 (Exit)")
        choice = Prompt.ask("", default="0").strip()

        if choice == "6":
            console.print("[dim]Exiting Life Mirror. Until next time. 🌱[/dim]")
            break

        elif choice == "4":
            enhanced_search(data)

        elif choice == "0":
            for idx, title in enumerate(titles):
                console.print(f"{len(titles)-idx}. {title}")
            handle_view_choice(data, titles)

        elif choice == "1":
            theme_map = {}
            console.print("\nEnter one of the following themes to explore:")
            for idx, (theme, items) in enumerate(categories.items()):
                key = chr(97 + idx)
                theme_map[key] = (theme, items)
                console.print(f"[{key.upper()}] {theme}")
            selected_key = Prompt.ask("Type the corresponding letter").strip().lower()
            if selected_key in theme_map:
                theme, items = theme_map[selected_key]
                console.print(Panel(f"[bold]{theme}[/bold] — {len(items)} conversations found.", style="bold blue", box=box.ROUNDED))
                for idx, title in items[-10:]:
                    console.print(f"{len(titles)-idx}. {title}")
                handle_view_choice(data, titles)
            else:
                console.print("[red]Invalid selection. Returning to menu.[/red]")

        elif choice == "2":
            console.print("\nHere are your most recent 10 conversations:")
            for i, title in enumerate(titles[-10:]):
                console.print(f"{len(titles) - (len(titles) - 10 + i)}. {title}")
            handle_view_choice(data, titles)

        elif choice == "3":
            console.print("\n[bold magenta]Unfinished Ideas or Follow-Ups:[/bold magenta]")
            for i, title in enumerate(titles):
                if any(word in title.lower() for word in ["idea", "draft", "request", "todo", "plan"]):
                    console.print(f"{len(titles)-i}. {title}")
            handle_view_choice(data, titles)

        elif choice == "5":
            idx = random.randint(0, len(data) - 1)
            view_chat_by_index(data, idx)

        else:
            console.print("[red]Invalid choice. Please enter a number between 0 and 6.[/red]")

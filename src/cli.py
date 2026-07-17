import sys
import webbrowser
from colorama import init, Fore, Style
from InquirerPy import inquirer
from scraper import search_media, get_tv_episodes, get_embed_url

init(autoreset=True)

def main():
    while True:
        print(Fore.MAGENTA + Style.BRIGHT + "\n🎬 67movies.net CLI")
        print(Fore.BLUE + "====================")
        choice = inquirer.select("What to do?", choices=["Movies", "TV Shows", "Exit"]).execute()
        if choice == "Exit":
            break

        media_type = "movie" if choice == "Movies" else "tv"
        query = inquirer.text("Enter title:").execute().strip()
        if not query:
            print(Fore.RED + "Please enter a search term.")
            continue

        results = search_media(query, media_type)
        if not results:
            print(Fore.RED + "No results found.")
            continue

        items = [f"{r['title']} ({r['year']})" for r in results]
        sel = inquirer.select("Select a title:", choices=items).execute()
        selected = next(r for r in results if f"{r['title']} ({r['year']})" == sel)

        if media_type == "movie":
            embed = get_embed_url("movie", selected["id"])
            if embed:
                print(Fore.GREEN + f"Opening in your browser:\n{embed}")
                webbrowser.open(embed)
            else:
                print(Fore.RED + "No embed URL found.")
        else:
            episodes = get_tv_episodes(selected["id"])
            if not episodes:
                print(Fore.RED + "No seasons found.")
                continue

            seasons = {s: data for s, data in episodes.items() if data["episodes"]}
            if not seasons:
                print(Fore.RED + "No episodes available.")
                continue

            season_str = inquirer.select(
                "Select season:",
                choices=[f"S{s} - {data['name']}" for s, data in seasons.items()]
            ).execute()
            season_num = int(season_str.split()[0][1:])
            ep_list = seasons[season_num]["episodes"]

            ep_str = inquirer.select(
                "Select episode:",
                choices=[f"E{e['episode_number']} - {e['name']}" for e in ep_list]
            ).execute()
            ep_num = int(ep_str.split()[0][1:])

            embed = get_embed_url("tv", selected["id"], season_num, ep_num)
            if embed:
                print(Fore.GREEN + f"Opening in your browser:\n{embed}")
                webbrowser.open(embed)
            else:
                print(Fore.RED + "No embed URL found.")

if __name__ == "__main__":
    main()
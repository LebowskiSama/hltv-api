import bs4
import requests

page = requests.get("https://www.hltv.org/matches")
soup = bs4.BeautifulSoup(page.content, "html.parser")


def fetchLive():

    live = []

    # Finding live matches
    liveMatches = soup.findAll("div", {"class": "live-match"})
    # print(live_matches)

    for match in liveMatches:
        # Find event title
        live_match_title = match.find("div", {"class": "event-name"})
        # Find BestOf
        bestof = match.find("td", {"class": "bestof"})
        # Find teams involved
        teams = match.findAll("span", {"class": "team-name"})
        teamnames = []
        for team in teams:
            teamnames.append(team)

        # Append dictionaries to the live list for each match
        live.append({
            "title": live_match_title.text,
            "bestof": bestof.text,
            "team1": teamnames[0].text,
            "team2": teamnames[1].text
        })

    return(live)

def fetchUpcoming():

    upcoming = []

    # Find upcoming matches
    upcomingMatches = soup.findAll("div", {"class": "match-day"})

    for event in upcomingMatches:
        # Find event date
        date = event.find("div", {"class": "standard-headline"})
        # Parse all upcoming match cards
        container = event.findAll("div", {"class": "upcoming-match"})

        event = []
        for item in container:

            # Find match title
            title = item.find("span", {"class": "event-name"})
            # Find match time
            time = item.find("td", {"class": "time"})
            # Find bestof and simultaneously handle exceptions for tbd events
            try:
                bestof = item.find("div", {"class": "map-text"}).text
                # Find teams involved and team logos
                teamnames = []
                teamlogos = []
                teams = item.findAll("div", {"class": "team"})
                teamicons = item.findAll("img", {"class": "logo"})
                for team in teams:
                    teamnames.append(team)
                for team in teamicons:
                    teamlogos.append(team["src"])

                # Error handling for when there's a lack of team logo
                try:                
                    event.append({
                        "time": time.text[1:-1],
                        "bestof": bestof,
                        "team1": teamnames[0].text[1:-1],
                        "team1logo": teamlogos[0],
                        "team2": teamnames[1].text,
                        "team2logo": teamlogos[1],
                        "tbd": 0
                    })
                except:
                # Present empty logos    
                    event.append({
                        "time": time.text[1:-1],
                        "bestof": bestof,
                        "team1": teamnames[0].text,
                        "team1logo": 0,
                        "team2": teamnames[1].text,
                        "team2logo": 0,
                        "tbd": 0
                    })

            # Error handling for tbd events
            except:
                title = item.find("td", {"class": "placeholder-text-cell"})
                event.append({
                    "time": time.text[1:-1],
                    "title": title.text,
                    "tbd": 1
                })
            pass

        upcoming.append(event)
        
    return(upcoming)
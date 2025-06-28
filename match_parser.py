from subprocess import run, CalledProcessError
from hoster import scrape_data


def filter_most_recent_match(data):
    """
    Filters out unplayed matches and returns the most recent match.

    :param data: The list of scraped match data
    :return: The most recent match (as a list)
    """
    # Filter out matches that have "00/00" or "00\xa0-\xa000"
    played_matches = [match for match in data if match[3] != "00\xa0-\xa000" and match[3] != ""]

    if not played_matches:
        return None  # No played matches found

    # Assuming the date is in the first column and in format 'dd/mm' (adjust as needed)
    last_match = played_matches[-1]  # Sort by date, descending

    # Return the most recent match
    return last_match


def main():
    latest_matches = []

    teams = {
        "ttc de pinte veteranen a": "7930_A",
        "ttc de pinte veteranen b": "7932_B",
        "ttc de pinte heren a": "7916_A",
        "ttc de pinte heren b": "7922_B",
        "ttc de pinte heren c": "7923_C",
        "ttc de pinte heren d": "7925_D",
        "ttc de pinte heren e": "7926_E",
        "ttc de pinte heren f": "7924_F",
        "ttc de pinte jeugd a": "7996_A",
        "ttc de pinte jeugd b": "7997_B",
        "ttc de pinte jeugd c": "7998_C"
    }

    for team in teams:
        url = ("https://competitie.vttl.be/index.php?menu=4&perteam=1&club_id=42&div_id=" + teams[
            team])  # Replace with your desired URL
        inputed = "resultaten"  # Filter parameter

        # Scrape data using the inputed variable
        scraped_data = scrape_data(url, inputed)

        # Filter the scraped data to get the most recent match
        if scraped_data and inputed == "resultaten":
            most_recent_match = filter_most_recent_match(scraped_data)

            if most_recent_match:
                latest_matches.append([most_recent_match, url])
            else:
                print(f"No played matches found for team {team}.")
        else:
            print(f"No data scraped or filtered for team {team}.")

    return latest_matches


if __name__ == "__main__":
    matches = main()
    for match in matches:
        print(match)

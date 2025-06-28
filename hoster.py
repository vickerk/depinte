import requests
from bs4 import BeautifulSoup


def scrape_data(url, inputed):
    """
    Scrapes data from the given URL and filters using the inputed parameter.

    :param url: The URL to scrape data from
    :param inputed: The value to filter for (e.g., 'resultaten')
    :return: A list of scraped match data
    """
    response = requests.get(url)
    should_register = False
    data = []

    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the section or table with "Resultaten"
    result_section = soup.find('section', {'id': 'resultaten'})  # Adjust if necessary

    # Alternatively, find all tables and filter the ones related to 'resultaten'
    tables = soup.find_all('table')

    # Loop through the tables to extract the relevant content
    for idx, table in enumerate(tables):
        rows = table.find_all('tr')

        # Loop through rows of the table
        times_registered = 0
        for row in rows:
            columns = row.find_all('td')
            if columns:
                column_data = [col.text.strip() for col in columns]
                if should_register and times_registered == 1:
                    if column_data[0].lower() not in ["resultaten", "spelers", "rangschikking", "totaal van de ploeg",
                                                      "verdeling van de scores", "aantal selecties in de ploeg", ] \
                            and "aantal" != column_data[0].lower().split(" ")[0]:
                        data.append(column_data)
                    else:
                        should_register = False
                elif column_data[0].lower() == inputed:
                    should_register = True
                    times_registered += 1

    return data

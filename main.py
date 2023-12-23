"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Petr Šplíchal
email: p.splichal98@gmail.com
discord: Petr Š
"""

from bs4 import BeautifulSoup
import requests
import sys
import csv

def main():
    """
    The function validates the given arguments and calls the scraping function
    """
    if not len(sys.argv) == 3:
        print(sys.argv)
        print("Neplatný počet argumentů!")
        quit()
    url = sys.argv[1]
    output_file = sys.argv[2]
    if not url.startswith('https://volby.cz'):
        print("Neplatný odkaz. Zadejte odkaz obsahující 'https://volby.cz'")
        quit()
    if not output_file.endswith(".csv") or len(output_file) <= 4:
        print("Neplatný název souboru!")
        quit()
    print(f"Stahuji data z vybraného URL: {url}")
    scraping(url, output_file)
    print(f"Ukládám do souboru: {output_file}\nUkončuji election-scraper")

def scraping(url_district, output_file):
    """
    :param url_district: url from 'https://volby.cz'
    :param output_file: name of output_file
    """
    response = requests.get(url_district)
    soup_district = BeautifulSoup(response.text, "html.parser")
    towns_numbers = scrape_town_number(soup_district)
    towns_names = scrape_town_name(soup_district)
    voters, envelopes, votes, all_parties, votes_for_parties = scrape_district_urls_precincts(soup_district)
    data_to_csv(towns_numbers, towns_names, voters, envelopes, votes, all_parties, votes_for_parties, output_file)

def scrape_town_number(soup_district):
    """
    :param soup_district: created object of type BeautifulSoup
    :return: list of towns numbers
    """
    town_numbers = []
    numbers = soup_district.find_all(name="td", class_="cislo")
    for number in numbers:
        town_numbers.append(number.text)
    return town_numbers

def scrape_town_name(soup_district):
    """
    :param soup_district: created object of type BeautifulSoup
    :return: list of towns names
    """
    town_names = []
    towns = soup_district.find_all(name="td", class_="overflow_name")
    for town in towns:
        town_names.append(town.text)
    return town_names

def scrape_district_urls_precincts(soup_district):
    """
    :param soup_district: created object of type BeautifulSoup
    :return: lists of voters, envelopes, valid votes, parties and votes for parties in urban precints
    """
    all_td = soup_district.find_all(name="td", class_="center")
    voters_in_precincts = []
    envelopes_in_precincts = []
    votes_in_precincts = []
    votes_for_parties = []
    for td in all_td:
        a = td.find(name="a")
        precint_url = a.get("href")
        full_precint_url = f"https://volby.cz/pls/ps2017nss/{precint_url}"
        voters, envelopes, votes, parties_names, all_votes = scrape_precincts(full_precint_url)
        voters_in_precincts.append(voters)
        envelopes_in_precincts.append(envelopes)
        votes_in_precincts.append(votes)
        votes_for_parties.append(all_votes)
    return voters_in_precincts, envelopes_in_precincts, votes_in_precincts, parties_names, votes_for_parties

def scrape_precincts(precinct_url):
    """
    :param precinct_url: url from 'https://volby.cz'
    :return: returns tallied lists of voters, envelopes, valid votes, parties, and votes for parties in town precints
    """
    precincts_total = []
    response = requests.get(precinct_url)
    soup_precinct = BeautifulSoup(response.text, "html.parser")
    if "vyber" in precinct_url:
        precinct = []
        precinct.append(scrape_voters(soup_precinct))
        precinct.append(scrape_envelopes(soup_precinct))
        precinct.append(scrape_votes(soup_precinct))
        precinct.append(scrape_votes_for_parties(soup_precinct))
        precincts_total.append(precinct)
    else:
        all_td = soup_precinct.find_all(name="td", class_="cislo")
        for td in all_td:
            precinct = []
            a = td.find(name="a")
            precinct_url = a.get("href")
            full_precinct_url = f"https://volby.cz/pls/ps2017nss/{precinct_url}"
            response = requests.get(full_precinct_url)
            soup_precinct = BeautifulSoup(response.text, "html.parser")
            precinct.append(scrape_voters(soup_precinct))
            precinct.append(scrape_envelopes(soup_precinct))
            precinct.append(scrape_votes(soup_precinct))
            precinct.append(scrape_votes_for_parties(soup_precinct))
            precincts_total.append(precinct)

    all_voters = 0
    all_envelopes = 0
    all_votes = 0
    all_votes_for_parties = [0] * 26

    for precinct in precincts_total:
        all_voters += precinct[0]
        all_envelopes += precinct[1]
        all_votes += precinct[2]
        index = 0
        for vote in precinct[3]:
            all_votes_for_parties[index] += vote
            index += 1
    all_parties = scrape_party_name(soup_precinct)
    return all_voters, all_envelopes, all_votes, all_parties, all_votes_for_parties

def scrape_voters(soup_precinct):
    """
    :param soup_precinct: created object of type BeautifulSoup
    :return: returns possible voters as an integer
    """
    voters = soup_precinct.find(name="td", class_="cislo", headers="sa2")
    return int(voters.text.replace("\xa0", ""))

def scrape_envelopes(soup_precinct):
    """
    :param soup_precinct: created object of type BeautifulSoup
    :return: returns issued envelopes as an integer
    """
    envelopes = soup_precinct.find(name="td", class_="cislo", headers="sa3")
    return int(envelopes.text)

def scrape_votes(soup_precinct):
    """
    :param soup_precinct: created object of type BeautifulSoup
    :return: returns valid votes as an integer
    """
    vote = soup_precinct.find(name="td", class_="cislo", headers="sa6")
    return int(vote.text)

def scrape_party_name(soup_precinct):
    """
    :param soup_precinct: created object of type BeautifulSoup
    :return: list of parties names
    """
    parties_names = []
    names_1 = soup_precinct.find_all(name="td", class_="overflow_name", headers="t1sa1 t1sb2")
    names_2 = soup_precinct.find_all(name="td", class_="overflow_name", headers="t2sa1 t2sb2")
    for name in names_1:
        parties_names.append(name.text)
    for name in names_2:
        parties_names.append(name.text)
    return parties_names

def scrape_votes_for_parties(soup_precinct):
    """
    :param soup_precinct: created object of type BeautifulSoup
    :return: list of votes for parties
    """
    parties_votes = []
    votes_1 = soup_precinct.find_all(name="td", class_="cislo", headers="t1sa2 t1sb3")
    votes_2 = soup_precinct.find_all(name="td", class_="cislo", headers="t2sa2 t2sb3")
    for vote in votes_1:
        parties_votes.append(int(vote.text))
    for vote in votes_2:
        parties_votes.append(int(vote.text))
    return parties_votes

def data_to_csv(numbers, names, voters, envelopes, votes, all_parties, all_votes_for_parties, output_file):
    """
    The function creates a csv file of the scraped data
    """
    headers = ["Číslo obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"]
    for party in all_parties:
        headers.append(party)

    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        for index in range(len(names)):
            row = [numbers[index], names[index], voters[index], envelopes[index], votes[index], *all_votes_for_parties[index]]
            csvwriter.writerow(row)

if __name__ == "__main__":
    main()
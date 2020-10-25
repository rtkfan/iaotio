import requests
from bs4 import BeautifulSoup
import locale
import random
import copy

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

UNCOUNTED_BALLOTS = 600000  # absentee/mail-in ballots, est. from Elections BC
NUM_TRIALS = 1000  # number of trials per electoral district
BIAS = -0.1 # bias (+ is toward BC Libs, - is toward BC NDP)

def assign_votes(party_list, split_electionday, num_votes):
    outlist = [0,0,0,0,0]
    bias_votes = int(sum(split_electionday)*BIAS)
    split_electionday[0] += bias_votes
    split_electionday[1] -= bias_votes

    for i in range(NUM_TRIALS):
        votelist = random.choices(party_list, split_electionday, k=num_votes)
        split_absentee = [len(list(filter(lambda x: x == p, votelist)))
                          for p in party_list]
        split_total = [sum(x) for x in zip(split_electionday, split_absentee)]
        winner = max(range(len(split_total)),key = split_total.__getitem__)
        outlist[winner] += 1
    return outlist

    # print(outlist)


# use live results -- copy these to stop hammering Elections BC ---------------
# page = requests.get('https://electionsbcenr.blob.core.windows.net/'
#                     'electionsbcenr/GE-2020-10-24_Party.html')
# with open('./datafile','w') as fwrite:
#     fwrite.write(page.text)
# soup = BeautifulSoup(page.text,'html.parser')
# -----------------------------------------------------------------------------

# use cached results ----------------------------------------------------------
with open('./datafile','r') as fread:
    pagetext = fread.read()

soup = BeautifulSoup(pagetext,'html.parser')
# -----------------------------------------------------------------------------

headers = [i.get_text() for i in soup.find('thead').find_all('th')]
parties = headers[2:7]

# there's only one tbody here
table = [i.find_all('td') for i in soup.find('tbody').find_all('tr')]
rows_str = [[i.get_text() for i in j] for j in table]

districts = [i[0] for i in rows_str]

vote_parties_electionday = [[locale.atoi(j) for j in i[2:7]] for i in rows_str]
vote_total_electionday = [sum(i) for i in vote_parties_electionday]

frac_ballots_electionday = [i/sum(vote_total_electionday)
                            for i in vote_total_electionday]
num_ballots_absentee = [int(UNCOUNTED_BALLOTS*i)
                        for i in frac_ballots_electionday]

for i in range(len(districts)):
    out_list = assign_votes(parties, vote_parties_electionday[i],
                            num_ballots_absentee[i])
    if out_list.count(0) != 4:
        print(districts[i],vote_parties_electionday[i],
              num_ballots_absentee[i], out_list)

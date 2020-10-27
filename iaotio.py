import requests
from bs4 import BeautifulSoup
import locale
import random
import copy
import logging

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S ',
                    level=logging.INFO)

UNCOUNTED_BALLOTS = 600000  # absentee/mail-in ballots, est. from Elections BC
NUM_TRIALS = 2000  # number of trials per electoral district
BIAS = [-0.1, -0.09, -0.08, -0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01,
        0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
# bias (+ is toward BC Libs, - is toward BC NDP)


def assign_votes(party_list, split_electionday, num_votes, party_bias=0):
    outlist = [0]*len(party_list)
    split_adjusted = copy.deepcopy(split_electionday)
    bias_votes = int(sum(split_electionday)*party_bias)
    split_adjusted[0] += bias_votes
    split_adjusted[1] -= bias_votes

    for i in range(NUM_TRIALS):
        votelist = random.choices(party_list, split_adjusted, k=num_votes)
        split_absentee = [len(list(filter(lambda x: x == p, votelist)))
                          for p in party_list]
        split_total = [sum(x) for x in zip(split_electionday, split_absentee)]
        winner = max(range(len(split_total)), key=split_total.__getitem__)
        outlist[winner] += 1
    return outlist

    # print(outlist)


# use live results -- copy these to stop hammering Elections BC ---------------
page = requests.get('https://electionsbcenr.blob.core.windows.net/'
                    'electionsbcenr/GE-2020-10-24_Party.html')
with open('./datafile', 'w') as fwrite:
    fwrite.write(page.text)
soup = BeautifulSoup(page.text, 'html.parser')
# -----------------------------------------------------------------------------

# use cached results ----------------------------------------------------------
# with open('./data/datafile', 'r') as fread:
#     pagetext = fread.read()
#
# soup = BeautifulSoup(pagetext, 'html.parser')
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

f = open('output.txt', 'w')

print('bias', 'electoral_district', 'election_night_leader', 'final_winner',
      'prob_winner', 'prob_lib', 'prob_ndp', 'prob_grn', 'prob_lbn',
      'prob_other', sep='\t', file=f)  # hard-code the header row

for ibias in BIAS:
    for i in range(len(districts)):
        logging.info(districts[i]+' @ bias='+str(ibias))
        iwinner = max(range(len(vote_parties_electionday[i])),
                      key=vote_parties_electionday[i].__getitem__)
        out_list = assign_votes(parties, vote_parties_electionday[i],
                                num_ballots_absentee[i], ibias)
        new_winner = max(range(len(out_list)), key=out_list.__getitem__)
        print(ibias, districts[i], parties[iwinner], parties[new_winner],
              out_list[new_winner]/NUM_TRIALS,
              out_list[0]/NUM_TRIALS, out_list[1]/NUM_TRIALS,
              out_list[2]/NUM_TRIALS, out_list[3]/NUM_TRIALS,
              out_list[4]/NUM_TRIALS,
              sep='\t', file=f, flush=True)

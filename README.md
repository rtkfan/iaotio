# iaotio (it ain't over 'til it's over)
Sensitivity analysis on absentee/mail-in ballots for 2020 British Columbia provincial election

View the results [on my Tableau Public profile](https://public.tableau.com/profile/matt.lam)

Due to COVID-19, there was a historically large number of absentee and mail-in ballots in the 2020 BC provincial election. Much has been made (by pundits and candidates, often on the 'losing' side) that this might materially affect the election results.

If we assume that the distribution of ballots is the same percentage-wise as on Election Day, then this is only true if the election-day result was a tight race, and if there were a large number of absentee/mail-in ballots. Problem is, the larger the number of the latter, then by the [law of large numbers](https://en.wikipedia.org/wiki/Law_of_large_numbers) it follows that the results will tend to the election-day average anyway.

This leads to the first question I'd like to answer: _Assuming that absentee/mail-in ballots are distributed similarly to those cast on Election Day, how likely is it that election results are affected?_

However, it seems likely that absentee/mail-in voters might be demographically different than Election Day voters, so there might be a difference in the result. For instance, one could argue that mail-in voters would lean BC Liberal, since their base skews older and they may want to minimize exposure to other people due to COVID-19.

This leads to our second question: _What happens to the election results if there's a global, systematic difference in voter preferences between Election Day and absentee/mail-in ballots?_

Here's the plan:
- Scrape Election Day ballot count from [Elections BC website](https://elections.bc.ca/), along with number of absentee/mail-in ballots
- Assume that absentee/mail-in ballots are distributed by Electoral District proportionally to votes cast on Election Day _(is this legit? I guess when the counts roll in for Final Count, we can update this to use actual number of ballots recorded)_
- Run a Monte Carlo analysis to see the likelihood of seats flipping based on election results, assuming that absentee/mail-in ballots are distributed like the Election Day result
- Bias the absentee/mail-in distributions toward BC NDP/BC Liberal, and repeat the Monte Carlo analysis to see how much bias needs to be introduced to materially affect the election results.

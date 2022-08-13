*Note: The images in this blog post are best viewed in dark mode. To switch to dark mode, click your name in the top right corner, click "Background", and select "Dark" or "Dark Board".*

*Acknowledgements: Thanks to [DevDarshanTK](https://lichess.org/@/DevDarshanTK) for pointing out that in the first two marathons, trophies were awarded only to top-50 finishers. This does not change the trophy rankings, but the text has been adjusted accordingly.*

## Introduction

With the [29th Lichess marathon](https://lichess.org/tournament/summer22) just behind us, with again over 22.000 participants, it seems that the magic of these rare day-long arenas (with special trophies for the highest ranking players!) has not yet worn off.

This blog post is about reflecting upon past marathons, with interesting statistics and plots, and about looking forward to future events, trying to make predictions about e.g. what scores may be needed to win certain trophies in the future.

Some questions that this blog post tries to answer include:

* Who have been the most successful in collecting marathon trophies in the past?
* Can we establish any trends from the results of past marathons?
* Can we make any predictions what someone needs to do to win a trophy in the future?

Although some other topics will also be discussed, the main focus is on the marathon trophies, which seem to be the main motivator for people to participate and play well.

## Data

For analyzing these marathons, let us first look at the data. The results of the following 29 marathons were used, which includes all marathons played to date, between the inaugural [Summer 2015 marathon](https://lichess.org/tournament/summer15) and the recently concluded [Summer 2022 marathon](https://lichess.org/tournament/summer22).

**Marathons**
The list below gives an overview of these arenas, the different time controls of these arenas, the number of participants, the average rating of the players, and the overall berserk rates. Various additional statistics about these arenas can also be found at [my Lichess statistics page](https://lichess.thijs.com/rankings/all/marathon/list_arenas_newest.html).

| **#** | **Arena ID** | **TC** | **Date** | **Players** | **Avg Rtng** | **Berserk** |
| --- | -------- | --- | ---- | ------- | -------- | ------- |
| 29. | [summer22](https://lichess.org/tournament/summer22) | 1+0 | Aug 05, 2022 | 22747 | 1718 | 7% |
| 28. | [spring22](https://lichess.org/tournament/spring22) | 2+1 | Apr 16, 2022 | 22560 | 1677 | 12% |
| 27. | [winter21](https://lichess.org/tournament/winter21) | 3+0 | Dec 28, 2021 | 28506 | 1764 | 18% |
| 26. | [autumn21](https://lichess.org/tournament/autumn21) | 3+2 | Oct 23, 2021 | 24377 | 1733 | 15% |
| 25. | [summer21](https://lichess.org/tournament/summer21) | 1+0 | Aug 07, 2021 | 24368 | 1655 | 7% |
| 24. | [spring21](https://lichess.org/tournament/spring21) | 5+0 | Apr 10, 2021 | 31332 | 1663 | 28% |
| 23. | [winter20](https://lichess.org/tournament/winter20) | 2+1 | Dec 28, 2020 | 27651 | 1606 | 12% |
| 22. | [autumn20](https://lichess.org/tournament/autumn20) | 3+0 | Oct 24, 2020 | 22454 | 1706 | 18% |
| 21. | [summer20](https://lichess.org/tournament/summer20) | 1+0 | Aug 01, 2020 | 20703 | 1669 | 7% |
| 20. | [spring20](https://lichess.org/tournament/spring20) | 2+1 | Apr 18, 2020 | 22497 | 1695 | 10% |
| 19. | [winter19](https://lichess.org/tournament/winter19) | 3+2 | Dec 28, 2019 | 13763 | 1713 | 10% |
| 18. | [autumn19](https://lichess.org/tournament/autumn19) | 3+2 | Oct 26, 2019 | 12175 | 1710 | 11% |
| 17. | [summer19](https://lichess.org/tournament/summer19) | 5+0 | Jul 06, 2019 | 12982 | 1634 | 23% |
| 16. | [spring19](https://lichess.org/tournament/spring19) | 3+0 | Mar 30, 2019 | 13439 | 1584 | 15% |
| 15. | [winter18](https://lichess.org/tournament/winter18) | 3+2 | Dec 29, 2018 | 13576 | 1579 | 11% |
| 14. | [autumn18](https://lichess.org/tournament/autumn18) | 5+0 | Oct 06, 2018 | 10792 | 1604 | 21% |
| 13. | [summer18](https://lichess.org/tournament/summer18) | 3+0 | Jul 07, 2018 | 9892 | 1642 | 13% |
| 12. | [spring18](https://lichess.org/tournament/spring18) | 5+0 | Mar 24, 2018 | 10055 | 1616 | 22% |
| 11. | [winter17](https://lichess.org/tournament/winter17) | 5+3 | Dec 28, 2017 | 9036 | 1620 | 17% |
| 10. | [autumn17](https://lichess.org/tournament/autumn17) | 3+2 | Oct 28, 2017 | 6815 | 1665 | 10% |
| 9. | [summer17](https://lichess.org/tournament/summer17) | 3+0 | Aug 13, 2017 | 6933 | 1695 | 12% |
| 8. | [spring17](https://lichess.org/tournament/spring17) | 3+2 | Apr 16, 2017 | 6766 | 1667 | 9% |
| 7. | [winter16](https://lichess.org/tournament/winter16) | 3+2 | Jan 08, 2017 | 6803 | 1679 | 9% |
| 6. | [autumn16](https://lichess.org/tournament/autumn16) | 3+2 | Oct 22, 2016 | 4630 | 1702 | 9% |
| 5. | [summer16](https://lichess.org/tournament/summer16) | 5+0 | Aug 06, 2016 | 4821 | 1707 | 16% |
| 4. | [spring16](https://lichess.org/tournament/spring16) | 5+0 | Apr 16, 2016 | 4119 | 1706 | 19% |
| 3. | [winter15](https://lichess.org/tournament/winter15) | 3+2 | Dec 28, 2015 | 4672 | 1608 | 8% |
| 2. | [autumn15](https://lichess.org/tournament/autumn15) | 3+0 | Oct 24, 2015 | 2802 | 1632 | 12% |
| 1. | [summer15](https://lichess.org/tournament/summer15) | 5+0 | Aug 01, 2015 | 2258 | 1572 | 13% |

**Time controls**
As we can see above, the marathons have been played at 6 different time controls so far:

* 1+0 (3 events)
* 2+1 (3 events)
* 3+0 (6 events)
* 3+2 (9 events)
* 5+0 (7 events)
* 5+3 (1 event)

As different time controls are mostly incomparable, we will extract various statistics for each time control separately, focusing on the first five time controls above - for the 5+3 time control there is only one marathon with this time control, making it impossible to draw any worthwhile conclusions for future 5+3 marathons.

**Data queries**
To get as much data as possible, the data that was used was all the data that could be obtained via the following Lichess API queries:

* `https://lichess.org/api/tournament/{id}` (general tournament info);
* `https://lichess.org/api/tournament/{id}?page={p}` for 1 <= p <= 50 (detailed score sheets).
* `https://lichess.org/api/tournament/{id}/results` (detailed results of all players);

More information could be obtained via `https://lichess.org/api/tournament/{id}/games` to get the PGN of all games, which includes e.g. the starting time of each game, which would allow for chronological time lines of scores throughout the 24h of a marathon. Given the slow speed of the Lichess API, fetching all the games for all marathons would unfortunately take a large amount of time, so for this blog post this additional data was not used.

## Statistics

Let us now get down to the juicy parts. What can we say about the data obtained via the API?

### **Participants per marathon**

First, a simple question: how did the number of participants evolve over time? The following figure shows the number of participants over time, showing a steady increase (as Lichess and online chess gained in popularity) until early 2020. Then, when the COVID-19 pandemic hit and lockdowns started happening across the world, we saw a surge in popularity of online chess, and also a strong increase in the participation of Lichess marathons.

Similar spikes in participation can be seen during the fall and winter of the Northern hemisphere of 2020 and 2021, when further lockdowns got more people sitting inside, entertaining themselves by playing chess online. In 2022, with most lockdowns having been lifted around the world, we see that the participation numbers are somewhat consistent with the previous 2015-2020 growth of Lichess marathon participation, extrapolated to 2022 - the increase in popularity due to COVID-19 seems to have mostly disappeared. This suggests that the linear trend, as drawn with the dashed line in the figure below, is a reasonably accurate depiction of the "regular" Lichess growth, when pandemics do not play a role, and how one might expect the number of players per marathon to develop in the future.

![image](https://lichess.thijs.com/marathons/plots/players.png)

### **Trophy winners**

What has perhaps inspired most players to play seriously in these marathons is the prospect of winning one of the rare Lichess trophies associated with finishing high enough in one of the marathons. Ever since the first marathon, all top-50 finishers received a special trophy for display on their profile, with even fancier trophies for those finishing in the the top 10 and winning the marathon.

After the second marathon, trophies were added for top-100 finishers as well, and after Lichess started growing more and more, and even finishing in the top 100 was becoming too hard for most players, Lichess decided to add a new trophy for top-500 finishers as well. These new trophies have been handed out since the [Summer 2021 marathon](https://lichess.org/tournament/summer21), and have *not* been awarded retroactively for past events - anyone finishing between positions 101 and 500 did not get any trophy before this marathon (nor did players finishing between 51 and 100 in the first two marathons).

Regarding tournament victories, as one can also see on [my Lichess arena statistics page](https://lichess.thijs.com/rankings/all/marathon/list_players_trophies.html), the legendary [Lance5500](https://lichess.org/@/Lance5500) has dominated the early marathons, giving him a big lead in the number of marathon victories over the rest of the field. In second place we have [Kastorcito](https://lichess.org/@/Kastorcito), [Valera\_B5](https://lichess.org/@/Valera_B5), and [Kolian222](https://lichess.org/@/Kolian222) with two marathon victories each.

Looking at the ranking of players according only to the *number* of trophies (with trophies for higher positions only being used to break ties), rather than tournament victories, we obtain the following different ranking. Here we also see [Lance5500](https://lichess.org/@/Lance5500) dominating the trophy count rankings, but some other community favorites are in the top as well, such as [Kingscrusher-YouTube](https://lichess.org/@/Kingscrusher-YouTube) (3), [penguingim1](https://lichess.org/@/penguingim1) (6), [EricRosen](https://lichess.org/@/EricRosen) (32), and everyone's favorite statistics-collector, [thijscom](https://lichess.org/@/thijscom) (23).

*EDIT: Due to cheaters being removed from the standings after the marathons finished, both [Alexr58](https://lichess.org/@/Alexr58) (#99 in [Winter 2020](https://lichess.org/tournament/winter20)) and [arvids\_andrejevs](https://lichess.org/@/arvids_andrejevs) (#99 in [Spring 2021](https://lichess.org/tournament/spring21)) missed out on one top-100 trophy. With this additional trophy, both would rank higher in the top 100, with Alexr58 taking #20 below.*

| **#** | **User** | **Trophies** | **#1** | **#10** | **#50** | **#100** | **#500** |
| --- | ---- | -------- | --- | --- | --- | ---- | ---- |
| 1. | [Lance5500](https://lichess.org/@/Lance5500) | **27** | 11 | 10 | 5 | 1 | 0 |
| 2. | [papasi](https://lichess.org/@/papasi) | **16** | 0 | 8 | 6 | 2 | 0 |
| 3. | [Kingscrusher-YouTube](https://lichess.org/@/Kingscrusher-YouTube) | **16** | 0 | 4 | 7 | 4 | 1 |
| 4. | [Lightlike](https://lichess.org/@/Lightlike) | **15** | 0 | 7 | 5 | 3 | 0 |
| 5. | [vovaches](https://lichess.org/@/vovaches) | **13** | 0 | 3 | 5 | 5 | 0 |
| 6. | [penguingim1](https://lichess.org/@/penguingim1) | **12** | 1 | 4 | 7 | 0 | 0 |
| 7. | [j\_coca](https://lichess.org/@/j_coca) | **12** | 0 | 1 | 6 | 3 | 2 |
| 8. | [Fritzi\_2003](https://lichess.org/@/Fritzi_2003) | **11** | 0 | 4 | 4 | 2 | 1 |
| 9. | [MrBug](https://lichess.org/@/MrBug) | **11** | 0 | 2 | 8 | 0 | 1 |
| 10. | [MeikeSchlecker](https://lichess.org/@/MeikeSchlecker) | **11** | 0 | 1 | 6 | 3 | 1 |
| 11. | [Chess-Network](https://lichess.org/@/Chess-Network) | **11** | 0 | 1 | 5 | 3 | 2 |
| 12. | [Galij](https://lichess.org/@/Galij) | **11** | 0 | 0 | 7 | 3 | 1 |
| 13. | [sincerity\_rules](https://lichess.org/@/sincerity_rules) | **11** | 0 | 0 | 2 | 6 | 3 |
| 14. | [DVRazor](https://lichess.org/@/DVRazor) | **10** | 0 | 1 | 6 | 2 | 1 |
| 15. | [marantz3](https://lichess.org/@/marantz3) | **10** | 0 | 1 | 4 | 2 | 3 |
| 16. | [ampronkin](https://lichess.org/@/ampronkin) | **10** | 0 | 0 | 6 | 3 | 1 |
| 17. | [dampooo](https://lichess.org/@/dampooo) | **9** | 0 | 1 | 5 | 0 | 3 |
| 18. | [GlazAlmaz](https://lichess.org/@/GlazAlmaz) | **9** | 0 | 1 | 3 | 4 | 1 |
| 19. | [GGbers](https://lichess.org/@/GGbers) | **9** | 0 | 0 | 2 | 4 | 3 |
| 20. | [chess-only-chess](https://lichess.org/@/chess-only-chess) | **8** | 0 | 1 | 7 | 0 | 0 |
| 21. | [GUROV-DMITRIY](https://lichess.org/@/GUROV-DMITRIY) | **8** | 0 | 0 | 4 | 3 | 1 |
| 22. | [BlackKnight98](https://lichess.org/@/BlackKnight98) | **8** | 0 | 0 | 4 | 3 | 1 |
| 23. | [thijscom](https://lichess.org/@/thijscom) | **8** | 0 | 0 | 3 | 1 | 4 |
| 24. | [TexasDeBrazil](https://lichess.org/@/TexasDeBrazil) | **8** | 0 | 0 | 1 | 4 | 3 |
| 25. | [Chesstrix01](https://lichess.org/@/Chesstrix01) | **8** | 0 | 0 | 1 | 3 | 4 |
| 26. | [Alexr58](https://lichess.org/@/Alexr58) | **8** | 0 | 0 | 0 | 6 | 2 |
| 27. | [ShahMatKanal](https://lichess.org/@/ShahMatKanal) | **7** | 0 | 6 | 1 | 0 | 0 |
| 28. | [Artem\_0degov](https://lichess.org/@/Artem_0degov) | **7** | 0 | 3 | 4 | 0 | 0 |
| 29. | [Spinaltap](https://lichess.org/@/Spinaltap) | **7** | 0 | 2 | 3 | 2 | 0 |
| 30. | [skulas](https://lichess.org/@/skulas) | **7** | 0 | 1 | 1 | 3 | 2 |
| 31. | [Maltinho](https://lichess.org/@/Maltinho) | **7** | 0 | 0 | 6 | 1 | 0 |
| 32. | [EricRosen](https://lichess.org/@/EricRosen) | **7** | 0 | 0 | 4 | 3 | 0 |
| 33. | [appelsinskall](https://lichess.org/@/appelsinskall) | **7** | 0 | 0 | 3 | 4 | 0 |
| 34. | [Hangemhigh](https://lichess.org/@/Hangemhigh) | **7** | 0 | 0 | 2 | 5 | 0 |
| 35. | [Takeda](https://lichess.org/@/Takeda) | **7** | 0 | 0 | 2 | 4 | 1 |
| 36. | [A\_H\_Kashefi](https://lichess.org/@/A_H_Kashefi) | **7** | 0 | 0 | 2 | 3 | 2 |
| 37. | [WattSchrott](https://lichess.org/@/WattSchrott) | **7** | 0 | 0 | 2 | 3 | 2 |
| 38. | [realcyberbird](https://lichess.org/@/realcyberbird) | **7** | 0 | 0 | 1 | 4 | 2 |
| 39. | [rondep](https://lichess.org/@/rondep) | **7** | 0 | 0 | 1 | 3 | 3 |
| 40. | [utf](https://lichess.org/@/utf) | **7** | 0 | 0 | 1 | 2 | 4 |

### Points for trophies

As the number of points varies greatly for different time controls, let us look at the number of points needed to obtain certain trophies, grouped by the different time controls.

**1+0**
First, for the most recent 1+0 marathons, we observe that the scores needed for top 50 and top 100 have been mostly unchanged over the past two years. The number of points required to reach the top 500 has gone up ever since the Summer 2021 marathon, where trophies for top 500 finishers were first introduced. For the marathon winners, we can only acknowledge the outstanding accomplishment of [Elda64](https://lichess.org/@/Elda64), who scored over 2000 points in the recent [Summer 2022 marathon](https://lichess.org/tournament/summer22), improving upon the point count of the previous 1+0 marathon winners by a considerable margin.

![image](https://lichess.thijs.com/marathons/plots/1+0_top.png)

**2+1**
In this semi-bullet time control, we again see a similar trend of scores for top 10, top 50, and top 100 being mostly consistent over the past two years, with a slight increase for the top-500 threshold due to the introduction of new trophies for top-500 finishers. We further see an increase in the number of points of the winners, showing that the prestige of the marathons is attracting strong players who are willing to invest a lot of time to win these events.

![image](https://lichess.thijs.com/marathons/plots/2+1_top.png)

**3+0**
For one of the most popular blitz time controls, where marathons date back all the way to 2015, we observe similar trends as above, with increasing points for each trophy ever since the marathons started. With the introduction of top-500 trophies, the scores for top 50 and top 100 seem to have stabilized here as well, while the threshold to reach the top 500 is much higher than before.

![image](https://lichess.thijs.com/marathons/plots/3+0_top.png)

**3+2**
For the 3+2 time control, we again observe similar patterns, with the thresholds for each trophy having increase quite considerably since the early days of Lichess. We further see a spike in the winner's score in [the Autumn 2019 marathon](https://lichess.org/tournament/autumn19) with the winner [Valera\_B5](https://lichess.org/@/Valera_B5) scoring a yet unsurpassed 800 points to win the event. The scores for each of the trophies has further gone up considerably when comparing pre-COVID and post-COVID numbers.

![image](https://lichess.thijs.com/marathons/plots/3+2_top.png)

**5+0**
Finally, for the traditional 5+0 time control, we notice how in the [Spring 2016 marathon](https://lichess.org/tournament/spring16), the winner [BahadirOzen](https://lichess.org/@/BahadirOzen) managed to score an astonishing 980 points, beating the then-#2 [Lance5500](https://lichess.org/@/Lance5500) by over 300 points! Trend-wise we again see a steady increase in the point thresholds needed to obtain each trophy, with significant gaps between the pre-COVID thresholds and the most recent score thresholds in the [Spring 2021 marathon](https://lichess.org/tournament/spring21).

![image](https://lichess.thijs.com/marathons/plots/5+0_top.png)

### **Ratings for trophies**

Besides the number of points that were needed to obtain certain trophies, let us also inspect the distribution of ratings for each trophy, to get an idea what trophies one might aim for with certain ratings. The ratings below are in the rating category corresponding to the marathon (bullet for 1+0 and 2+1, and blitz for 3+0, 3+2, and 5+0). The below analyses have been performed only on the most recent marathons in each time control, as these are likely the best predictors for future events.

**1+0**
The most recent [Summer 2022 marathon](https://lichess.org/tournament/summer22) had the following characteristics in terms of the rating distributions among the different trophies. We note that all top 10 finishers were 2700 or higher (with the bulk being 2800+), that most top-50 and top-100 finishers were 2600+, and that the top 500 mostly consists of players in the rating range 2200-2500. No one rated below 2000 made it to any of the trophies in the most recent marathon.

![image](https://lichess.thijs.com/marathons/plots/summer22_rating_violin.png)

**2+1**
In the 2+1 [Spring 2022 marathon](https://lichess.org/tournament/spring22), which also falls under the bullet category, we notice that ratings were overall considerably lower. The ratings of the top-10 finishers were considerably lower than for the [Summer 2022 marathon](https://lichess.org/tournament/summer22), and to an extent this is also true for the other trophy categories. One explanation may be that most serious chess players dislike 2+1 as a (bullet) time control, whereas 1+0 gets even the best players excited to participate. Another explanation may be that in 2+1 it is relatively hard to berserk and win, due to the loss of increment, which makes it harder for strong players to make it to the top positions with a small number of games (and a high berserk percentage).

![image](https://lichess.thijs.com/marathons/plots/spring22_rating_violin.png)

**3+0**
For the blitz-rated 3+0 [Winter 2021 marathon](https://lichess.org/tournament/winter21), the ratings were overall quite high, considering that blitz ratings generally tend to be a bit lower than bullet ratings. This may again be related to 3+0 being a popular blitz time control among top players, and therefore attracting many strong players as well. We notice that also here, players rated below 2000 were not able to take any of the trophies, while everyone in the top 10 was rated 2550+.

![image](https://lichess.thijs.com/marathons/plots/winter21_rating_violin.png)

**3+2**
Similar to 2+1 and 1+0, we observe that 3+2 seems to be less popular among strong players than 3+0, with lower-rated players winning a larger number of trophies compared to 3+0 marathons. Some players rated below 2000 (blitz) were even able to win top 500 trophies in the [Autumn 2021 marathon](https://lichess.org/tournament/autumn21), and the winner [Kolian222](https://lichess.org/@/Kolian222) had a relatively low rating compared to the winner of the 3+0 [Winter 2021 marathon](https://lichess.org/tournament/winter21).

![image](https://lichess.thijs.com/marathons/plots/autumn21_rating_violin.png)

**5+0**
Finally, as 5+0 is also a community favorite for blitz chess, we again see relatively high ratings for top trophy winners in the [Spring 2021 marathon](https://lichess.org/tournament/spring21). We note that for this marathon, trophies did not yet exist for top 500 finishers, which may explain why the ratings were relatively low and spread out in the top 500 distribution. For the upcoming [Autumn 2022 marathon](https://lichess.org/tournament/autumn22) the latter distribution may therefore look very different, as more higher-rated players may push harder to win that trophy, taking away the trophies from lower-rated players.

![image](https://lichess.thijs.com/marathons/plots/spring21_rating_violin.png)

### Games per trophy (per rating)

Let us also take a look at how many games one has to play to win a trophy, and how the number of games correlates with the rating of the player winning the trophy. We will again work with the most recent marathons in the corresponding time controls to illustrate these relations.

**1+0**
As the following figure shows, unsurprisingly one generally needs more games to win any of the trophies when rated lower. For higher trophies one needs to play even more games, and/or be rated even higher. We observe that the winner [Elda64](https://lichess.org/@/Elda64) of the [Summer 2022 marathon](https://lichess.org/tournament/summer22) played over 800 games, making them one of the players in the top 500 with the most games played. Together with their high rating, this led to the impressive score of >2000 points.

![image](https://lichess.thijs.com/marathons/plots/summer22_rating_games.png)

**2+1**
For 2+1 we see similar relations as in the 1+0 time control, with higher-rated players needing fewer games to win each of the different trophies. We notice one outlier in the number of games: [cheetosss](https://lichess.org/@/cheetosss) played 532 games to finish 32nd with a rating of "only" 2221, showing that dedication to win these trophies sometimes does pay off! The highest-rated player of the top 500, [HomayooonT](https://lichess.org/@/HomayooonT), managed to win the marathon, needing only a moderate number of games (296 games) to do this.

![image](https://lichess.thijs.com/marathons/plots/spring22_rating_games.png)

**3+0**
For the 3+0 [Winter 2021 marathon](https://lichess.org/tournament/winter21) we again see similar trends in terms of higher trophies requiring more games and higher ratings to achieve them. We notice one yellow (top 10) outlier, needing only 239 games to make it to the top 10: with a final sprint and 99% berserking, [Lance5500](https://lichess.org/@/Lance5500) barely made it into the top 10 to win that extra trophy!

![image](https://lichess.thijs.com/marathons/plots/winter21_rating_games.png)

**3+2**
For the 3+2 time control we again observe similar patterns, with only few outliers this time. The highest-rated player, making it into the top 50 with only 108 games, was [NeverEnough](https://lichess.org/@/NeverEnough). The winner [Kolian222](https://lichess.org/@/Kolian222) had the lowest rating out of the top 10, but also played the most games out of the top-10 finishers to take the top prize.

![image](https://lichess.thijs.com/marathons/plots/autumn21_rating_games.png)

**5+0**
In the [Spring 2021 marathon](https://lichess.org/tournament/spring21) we again see familiar trends. The two people rated below 1900 and making it to the top 500 had to play around 300 games to do it, compared to a few players rated 2600+ and playing less than 100 games to make it to the top 500. The winner [Kastorcito](https://lichess.org/@/Kastorcito) found the right balance between playing the best and the most chess, with a high rating and a large number of games.

![image](https://lichess.thijs.com/marathons/plots/spring21_rating_games.png)

## Predictions

Based on the above statistics, we can try to make predictions for the future. Perhaps the most burning question to many is: how many arena points will I need to win certain trophies in future marathons? How many points would be needed to win, and to make the top 10/50/100/500? How many games would I need to play for that? And how strong does someone need to be to win one of these trophies?

Although there is not enough data to draw rigorous conclusions, one can try to extrapolate from past results, keeping in mind that participation in the future may vary greatly. For instance, in recent years Lichess has gained in popularity, leading to more participants and higher scores, and during COVID-19 lockdowns participation was even higher. Any future pandemic-related lockdowns may greatly influence participation, and the required score to win a trophy. Any predictions below must therefore be taken with a large grain of salt, and are dependent on various factors beyond the scope of this analysis.

That said, based on past results, let us make a rough prediction for the scores needed to win trophies in marathons at various time controls. These predictions exclude the 5+3 time control, for which we only have one data point, and which is a time control which will likely (hopefully) never return to the marathon format.

Below is a table with the estimated scores (number of arena points) needed to win the five types of trophies, for the five main time controls of marathons. These are mostly based on the above figures of the scores needed to win each trophy at each time control, and making a rough extrapolation based on those results.

| **TC** | **Winner** | **Top 10** | **Top 50** | **Top 100** | **Top 500** |
| --- | ------ | ------ | ------ | ------- | ------- |
| 1+0 | 2000+ | 1000-1100 | 750-800 | 700-750 | 500-550 |
| 2+1 | 900+ | 500-600 | 400-450 | 350-400 | 250-300 |
| 3+0 | 1100+ | 650-750 | 450-500 | 400-450 | 300-350 |
| 3+2 | 700+ | 400-500 | 300-350 | 250-300 | 200-250 |
| 5+0 | 800+ | 500-600 | 400-450 | 350-400 | 200-250\* |

With the [upcoming Autumn 2022 marathon](https://lichess.org/tournament/autumn22) having a 5+0 time control, one may for instance estimate that to win the event, one needs 800+ points to be sure, while to make the top 500, the threshold will lie somewhere between 200 and 250 points. Note however that the extrapolation for the top 500 for 5+0 has a high degree of uncertainty, as there have not been any 5+0 marathons in the past where the top 500 won a trophy. It is quite possible that, with these new trophies and this new motivation to make it to the top 500, the threshold for reaching the top 500 will lie even higher than 250 points.

Using the aforementioned graphs of the relation between ratings and games needed to win certain trophies, one can also draw conclusions w.r.t. how many games one would need to play at various rating ranges, to make it to the trophies. As this depends on many factors (ratings, games, time control), we will leave these estimates to the reader, who can use the figures in this blog post to make their own predictions.

## Conclusions

Although 29 marathons (played at various time controls) is not a lot of data to make accurate predictions, the analyses above and the plots suggest that there are some clear trends visible in these marathons. We observed how the COVID-19 pandemic has affected participation, how the increased participation (and the introduction of trophies for top-500 finishers) has raised the bar for each of the different trophies, and we made some rough predictions how many points may be needed to make it to certain trophies in the future.

Overall, hopefully these statistics were interesting and insightful to read, and hopefully this data helps you in estimating what you need to do in the future to win one of these trophies yourself!

*For more statistics, please don't forget to check out [my Lichess arena statistics pages](https://lichess.thijs.com/rankings/all/marathon/list_players_trophies.html). For instance, did you know that there are only [two players](https://lichess.thijs.com/rankings/all/marathon/list_players_events.html) who played more marathons than [Lance5500](https://lichess.org/@/Lance5500) (28 vs. Lance's 27)? Or that [EricRosen](https://lichess.org/@/EricRosen) is in the top 10 of [most points scored in all marathons combined](https://lichess.thijs.com/rankings/all/marathon/list_players_points.html)?* *These statistics pages include thousands of tables and graphs of different types of arenas played at different time controls, with more information than you'll ever need!*

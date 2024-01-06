<h3>1</h3>
This code validates equity intraday calls in AngelOneAdvisory telegram group.

These are the 6 things this code does:

1.Messages are fetched from telegram AngelOneAdvisor group using telethon(telthon is a python library which uses the telegram api).

2.Then the necessary fields like date & time,equity name, SL , TGT and PRICE are extracted.

3.Then using smart api (which is the api of AngelOne) the data of the day the message was sent and after the time the message was sent is fetched for that 
particular stock.

4.Then it is checked to see if SL or target was achieved if neither then, whether the call turned out to be a profit or loss on exit is 
checked(3:20 is taken as the exit time).

5.Then two plots are done ,one is profit/loss plot the other is risk to reward.

6.Finally days.txt is updated. days.txt contains two values for every weekday one is the number of messages on that particular day and the
other is the net profit or loss on that particular days.

Things to note:

1.This code only validates intraday buy/sell calls but it can be extended to handle all the messages.

2.Also this is only done for equity this also can be extended.
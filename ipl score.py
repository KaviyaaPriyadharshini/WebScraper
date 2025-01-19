from bs4 import BeautifulSoup
import requests
import pandas as pd
import select

url="https://www.espncricinfo.com/live-cricket-score"

Headers=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'})

webpage=requests.get(url,headers=Headers)

soup=BeautifulSoup(webpage.content,"html.parser")

team1=soup.find("p",attrs={'class':'ds-text-tight-m ds-font-bold ds-capitalize ds-truncate !ds-text-typo-mid3'}).text


team2=soup.find("p",attrs={'class':'ds-text-tight-m ds-font-bold ds-capitalize ds-truncate'}).text

print("Match Between '",team1.upper(),"' And '",team2.upper(),"'")

url1="https://m.cricbuzz.com/cricket-commentary/66369/gt-vs-lsg-30th-match-indian-premier-league-2023"

new_webpage=requests.get(url1,headers=Headers)

new_soup=BeautifulSoup(new_webpage.content,"html.parser")

score1=new_soup.find('span',attrs={'class':'teamscores ui-bowl-team-scores'}).text

print(score1)

score2=new_soup.find('span',attrs={'class':'miniscore-teams ui-bat-team-scores'}).text

print(score2)

commentry=new_soup.find('div',attrs={'class':'cbz-ui-status'}).text

print(commentry)

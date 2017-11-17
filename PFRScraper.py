#python "C:\Users\danie\Dropbox\Projects\NFL Racial Bias\PFRScraper.py"

import pandas as pd
import re
from requests import get
import math

urls = [
  'https://www.pro-football-reference.com/players/L/LeafRy00.htm',
  'https://www.pro-football-reference.com/players/M/MannPe00.htm',
  'https://www.pro-football-reference.com/players/K/KaepCo00.htm',
  'https://www.pro-football-reference.com/players/M/MannEl00.htm',
  'https://www.pro-football-reference.com/players/T/TaylTy00.htm',
  'https://www.pro-football-reference.com/players/S/SmitAl03.htm',
  'https://www.pro-football-reference.com/players/B/BortBl00.htm',
  'https://www.pro-football-reference.com/players/G/GrifRo01.htm',
  'https://www.pro-football-reference.com/players/L/LuckAn00.htm',
  'https://www.pro-football-reference.com/players/R/RivePh00.htm',
  'https://www.pro-football-reference.com/players/B/BreeDr00.htm',
  'https://www.pro-football-reference.com/players/M/McCoJo01.htm',
  'https://www.pro-football-reference.com/players/C/CutlJa00.htm',
  'https://www.pro-football-reference.com/players/F/FitzRy00.htm',
  #'https://www.pro-football-reference.com/players/H/HoyeBr00.htm',
  'https://www.pro-football-reference.com/players/D/DaltAn00.htm',
  'https://www.pro-football-reference.com/players/F/FlacJo00.htm',
  'https://www.pro-football-reference.com/players/K/KeenCa00.htm',
  'https://www.pro-football-reference.com/players/C/CarrDe02.htm',
  'https://www.pro-football-reference.com/players/C/CarrDa00.htm',
  'https://www.pro-football-reference.com/players/L/LosmJ.00.htm',
  'https://www.pro-football-reference.com/players/N/NewtCa00.htm',
  'https://www.pro-football-reference.com/players/W/WinsJa00.htm',
  'https://www.pro-football-reference.com/players/M/MariMa01.htm'
  
]

frames=[]
for url in urls:
  this_player = url.split('/')
  this_player = this_player[len(this_player)-1].split('.')[0]
  print( this_player )
  
  web         = get(url)
  all_data    = pd.read_html(web.text)
  if all_data[0].columns[0] == 'Year':
    data        = all_data[0]
  else:
    data        = all_data[1]

  data            = data.loc[ ~(pd.isnull(data['QBrec']))]
  #data['QBrec2']  = data['QBrec'].apply(lambda x: ''.join(['\'', str(x)]))
  data['Year2']   = data['Year'].apply( lambda x: re.sub("[^0-9]", "", x) )
  data            = data.loc[data['Year2'] != '']

  #print(data)
  data['Wins']    = data['QBrec'].apply( lambda x: str(x).split('-')[0] )
  data['Losses']  = data['QBrec'].apply( lambda x: str(x).split('-')[1] )
  data['Ties']    = data['QBrec'].apply( lambda x: str(x).split('-')[2] )
  
  cols            = [ 'Year2', 'GS', 'Cmp', 'Att', 'Cmp%', 'Rate', 'ANY/A', 'Wins', 'Losses', 'Ties']
  data_red        = data[cols]
  data_red['Player'] = this_player
  data_red        = data_red.reset_index()
  frames.append(data_red)

all_data  = pd.concat(frames)
all_data.to_csv('C:\\Users\\danie\\Dropbox\\Projects\\NFL Racial Bias\\all_data.csv')
print( all_data )
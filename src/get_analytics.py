import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import os


def get_data(player, start_date, end_date=None):
    if not os.path.exists("../stats/" + player):
        os.mkdir("../stats/" + player)
    if end_date is None:
        end_date = start_date
    
    df_jump = pd.read_csv("../data/2017_GAMES_JUMP_MASTER.csv", index_col=1)
    df_jump = df_jump.loc[:, ~df_jump.columns.str.contains('^Unnamed')]
    
    df_jump.index = pd.to_datetime(df_jump.index)
    player_data = df_jump.loc[(df_jump['player name'] == player)]
    player_data = player_data[start_date : end_date]

    # print(player_data["height (in)"].mean())

    df_jump_average = df_jump.groupby(['date', 'player name'])['height (in)'].mean().reset_index(name='Daily height Average')
    
    player_jump_data = df_jump_average.loc[(df_jump_average['player name'] == player)]
    del player_jump_data['player name']
    player_jump_data = player_jump_data.set_index('date')
    ax = player_jump_data.plot(title="Mean Jump Height for " + player)		    		  		  		    	 		 		   		 		  
    ax.set_xlabel("Date")  		   	  			    		  		  		    	 		 		   		 		  
    ax.set_ylabel('height') 
    plt.savefig("../stats/" + player + "/Jump_Height.png")

def email_players():
    pass

def email_coaches():
    pass

if __name__ == "__main__":
    df_jump = pd.read_csv("../data/2017_GAMES_JUMP_MASTER.csv", index_col=1)
    players = set(df_jump['player name'].values)
    if not os.path.exists("../stats"):
        os.mkdir("../stats")
    for player in players:
        get_data(player, '10/1/2017', '11/24/2017')
    # np.datetime64('2017-10-01'), np.datetime64('2017-11-24'))


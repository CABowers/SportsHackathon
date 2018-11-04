import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import os


def get_jump_data(player, start_date, end_date=None):
    if not os.path.exists("../stats/" + player):
        os.mkdir("../stats/" + player)
    if end_date is None:
        end_date = start_date
    
    df_jump = pd.read_csv("../data/2017_GAMES_JUMP_MASTER.csv", index_col=1)
    df_jump = df_jump.loc[:, ~df_jump.columns.str.contains('^Unnamed')]
    
    df_jump.index = pd.to_datetime(df_jump.index)

    team_jump_average = df_jump[start_date: end_date].groupby(['date'])['height (in)'].mean().reset_index(name='Team').set_index('date')

    if player == "Team":
        ax = team_jump_average.plot(title="Mean Jump Height for " + player)		    		  		  		    	 		 		   		 		  
        ax.set_xlabel("Date")  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_ylabel('height') 
        plt.savefig("../stats/" + player + "/Jump_Height.png")
        plt.cla()
    else:

        player_data = df_jump.loc[(df_jump['player name'] == player)]
        player_data = player_data[start_date : end_date]

        # print(player_data["height (in)"].mean())

        df_jump_average = df_jump.groupby(['date', 'player name'])['height (in)'].mean().reset_index(name=player)
        
        player_jump_data = df_jump_average.loc[(df_jump_average['player name'] == player)]
        del player_jump_data['player name']
        player_jump_data = player_jump_data.set_index('date')
        ax = player_jump_data.join(team_jump_average).plot(title="Mean Jump Height for " + player)		    		  		  		    	 		 		   		 		  
        ax.set_xlabel("Date")  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_ylabel('height') 
        plt.savefig("../stats/" + player + "/Jump_Height.png")
        plt.cla()

    

def get_impact_data(player, start_date, end_date=None):
    if not os.path.exists("../stats/" + player):
        os.mkdir("../stats/" + player)
    if end_date is None:
        end_date = start_date
    
    df_impact = pd.read_csv("../data/2017_GAME_IMPACT_MASTER.csv", index_col=0)
    df_impact = df_impact.loc[:, ~df_impact.columns.str.contains('^Unnamed')]
    df_impact.index = pd.to_datetime(df_impact.index)
    
    team_impact_average = df_impact[start_date: end_date].groupby(['date'])['gforce (G)'].mean().reset_index(name='Team').set_index('date')

    if player == "Team":
        ax = team_impact_average.plot(title="Mean GForce for " + player)		    		  		  		    	 		 		   		 		  
        ax.set_xlabel("Date")  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_ylabel('height') 
        plt.savefig("../stats/" + player + "/GForce.png")
        plt.cla()
    else:
        player_data = df_impact.loc[(df_impact['player name'] == player)]
        player_data = player_data[start_date : end_date]

        # print(player_data["gforce (G)"].mean())

        df_impact_average = df_impact.groupby(['date', 'player name'])['gforce (G)'].mean().reset_index(name=player)
        player_impact_data = df_impact_average.loc[(df_impact_average['player name'] == player)]
        del player_impact_data['player name']
        player_impact_data = player_impact_data.set_index('date')
        ax = player_impact_data.join(team_impact_average).plot(title="Mean GForce for " + player)		    		  		  		    	 		 		   		 		  
        ax.set_xlabel("Date")  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_ylabel('GForce') 
        plt.savefig("../stats/" + player + "/GForce.png")
        plt.cla()

def get_summary_data(player, start_date, end_date):
    if not os.path.exists("../stats/" + player):
        os.mkdir("../stats/" + player)
    if end_date is None:
        end_date = start_date
    
    df_summary = pd.read_csv("../data/match_nc_state_load_summary_clean.csv", index_col=20)
    # df_summary = df_impact.loc[:, ~df_impact.columns.str.contains('^Unnamed')]
    df_summary.index = pd.to_datetime(df_summary.index)
    df_summary["Energy per Inched Jump"] = df_summary["Kinetic Energy (Joules/Pound)"] / (df_summary["Jumps"] * df_summary["Avg Jump (in)"])

    print(df_summary[["Player Name","Energy per Inch Jump"]])
    player_data = df_summary.loc[(df_summary['Player Name'] == player)]
    player_data = player_data[start_date : end_date]
    player_data["Energy per Jump Inch"] = player_data["Kinetic Energy (Joules/Pound)"] / (player_data["Jumps"] * player_data["Avg Jump (in)"])
    
def get_stats_fancy():
    pass

def email_players():
    pass

def email_coaches():
    pass

if __name__ == "__main__":
    # get_jump_data("Gabby Benda", '10/01/2017', '11/28/2017')
    
    df_jump = pd.read_csv("../data/2017_GAMES_JUMP_MASTER.csv", index_col=1)
    players = set(df_jump['player name'].values)
    if not os.path.exists("../stats"):
        os.mkdir("../stats")
    for player in players:
        get_jump_data(player, '10/1/2017', '11/24/2017')
    # print(players)
    df_impact = pd.read_csv("../data/2017_GAME_IMPACT_MASTER.csv", index_col=1)
    players = set(df_impact['player name'].values)
    # print(players)
    for player in players:
        get_impact_data(player, '10/1/2017', '11/24/2017')
    
    

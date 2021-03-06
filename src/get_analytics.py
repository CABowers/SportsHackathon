import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import os
import re


def get_jump_data(player, start_date, end_date=None):
    if not os.path.exists("../stats/" + player):
        os.mkdir("../stats/" + player)
    kind="line"
    if end_date is None:
        kind="bar"
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
        plt.close()
    else:

        player_data = df_jump.loc[(df_jump['player name'] == player)]
        player_data = player_data[start_date : end_date]

        # print(player_data["height (in)"].mean())

        df_jump_average = df_jump.groupby(['date', 'player name'])['height (in)'].mean().reset_index(name=player)
        
        player_jump_data = df_jump_average.loc[(df_jump_average['player name'] == player)]
        del player_jump_data['player name']
        player_jump_data = player_jump_data.set_index('date')
        ax = player_jump_data.join(team_jump_average).plot(title="Mean Jump Height for " + player, kind=kind)		    		  		  		    	 		 		   		 		  
        ax.set_xlabel("Date")  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_ylabel('height') 
        plt.savefig("../stats/" + player + "/Jump_Height.png")
        plt.close()

    

def get_impact_data(player, start_date, end_date=None):
    if not os.path.exists("../stats/" + player):
        os.mkdir("../stats/" + player)
    kind="line"
    if end_date is None:
        kind="bar"
        end_date = start_date
    
    # df_impact = pd.read_csv("../data/2017_GAME_IMPACT_MASTER.csv", index_col=0)
    df_impact = pd.read_csv("../data/match_impact_master.csv", index_col=0)

    df_impact = df_impact.loc[:, ~df_impact.columns.str.contains('^Unnamed')]
    df_impact.index = pd.to_datetime(df_impact.index)
    
    team_impact_average = df_impact[start_date: end_date].groupby(['date'])['gforce (G)'].mean().reset_index(name='Team').set_index('date')

    if player == "Team":
        ax = team_impact_average.plot(title="Mean GForce for " + player)		    		  		  		    	 		 		   		 		  
        ax.set_xlabel("Date")  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_ylabel('height') 
        plt.savefig("../stats/" + player + "/GForce.png")
        plt.close()
    else:
        player_data = df_impact.loc[(df_impact['player name'] == player)]
        player_data = player_data[start_date : end_date]

        # print(player_data["gforce (G)"].mean())

        df_impact_average = df_impact.groupby(['date', 'player name'])['gforce (G)'].mean().reset_index(name=player)
        player_impact_data = df_impact_average.loc[(df_impact_average['player name'] == player)]
        del player_impact_data['player name']
        player_impact_data = player_impact_data.set_index('date')
        ax = player_impact_data.join(team_impact_average).plot(title="Mean GForce for " + player, kind=kind)		    		  		  		    	 		 		   		 		  
        ax.set_xlabel("Date")  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_ylabel('GForce') 
        plt.savefig("../stats/" + player + "/GForce.png")
        plt.close()

def get_summary_data(player, attribute, start_date, end_date):
    if not os.path.exists("../stats/" + player):
        os.mkdir("../stats/" + player)
    kind="line"
    if end_date is None:
        kind="bar"
        end_date = start_date
    
    df_summary = pd.read_csv("../data/master_summary.csv", index_col=20)
    df_box = pd.read_csv("../data/box_score_master.csv", index_col=1)
    df_summary.index = pd.to_datetime(df_summary.index)
    df_summary["Energy per Inched Jump"] = df_summary["Kinetic Energy (Joules/Pound)"] / (df_summary["Jumps"] * df_summary["Avg Jump (in)"])
    
    df_summary = df_summary[start_date: end_date].replace(np.inf, np.NaN).replace(0, np.NaN)

    team_attribute_average = df_summary.groupby(['date'])[attribute].mean().reset_index(name='Team').set_index('date')
    if player == "Team":
        df_attribute_average = df_summary.groupby(['Player Name'])[attribute].mean().reset_index(name=attribute)
        df_attribute_average = df_attribute_average.set_index("Player Name")
        title = attribute.split("(")[0]
        ax = df_attribute_average.plot(x=None, y=None, title=attribute + " for " + player, kind="pie", subplots=True, legend=False, sharey=False, sharex=False)		    		  		  		    	 		 		   		 		  
        plt.axes().set_ylabel('')
        plt.savefig("../stats/" + player + "/"+ title +".png")
        plt.close()
        return
    
    player_data = df_summary.loc[(df_summary['Player Name'] == player)]
    player_data = player_data[start_date : end_date]


    if not player_data.empty:

        df_attribute_average = df_summary.groupby(['date', 'Player Name'])[attribute].mean().reset_index(name=player)
        player_attribute_data = df_attribute_average.loc[(df_attribute_average['Player Name'] == player)]
        del player_attribute_data['Player Name']
        player_attribute_data = player_attribute_data.set_index('date')
        title = attribute.split("(")[0]
        ax = player_attribute_data.join(team_attribute_average).plot(title=title + " for " + player, kind=kind)		    		  		  		    	 		 		   		 		  
        ax.set_xlabel("Date")  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_ylabel(attribute) 
        plt.savefig("../stats/" + player + "/"+ title +".png")
        plt.close()


def get_box_data(player, attribute, start_date, end_date):
    if not os.path.exists("../stats/" + player):
        os.mkdir("../stats/" + player)
    kind="line"
    if end_date is None:
        kind="bar"
        end_date = start_date
    
    df_summary = pd.read_csv("../data/box_score_master.csv", index_col=1)
    df_summary.index = pd.to_datetime(df_summary.index)
    # print(df_summary)
    player_data = df_summary.loc[(df_summary['Player'] == player)]
    player_data = player_data[start_date : end_date]
    totals = df_summary.loc[(df_summary['Player'] == "Totals")][start_date : end_date]
    df_summary = df_summary[start_date : end_date]
    if not player_data.empty:
        
        df_attribute_average = df_summary.groupby(['Game_Date', 'Player'])[attribute].mean().reset_index(name=player)
        player_attribute_data = df_attribute_average.loc[(df_attribute_average['Player'] == player)]
        df_attribute_average = df_summary.groupby(['Game_Date', 'Player'])[attribute].mean().reset_index(name="Total")
        total_attribute_data = df_attribute_average.loc[(df_attribute_average['Player'] == 'Totals')]
        df_summary = df_summary[df_summary["Player"] != "Totals"]
        df_average = df_summary.groupby(['Game_Date'])[attribute].mean().reset_index(name="Team AVG")
        del player_attribute_data['Player']
        del total_attribute_data['Player']
        player_attribute_data = player_attribute_data.set_index('Game_Date')
        total_attribute_data = total_attribute_data.set_index('Game_Date')
        df_average = df_average.set_index("Game_Date")
        ax = player_attribute_data.join(df_average).plot(title=attribute + " for " + player, kind=kind)		    		  		  		    	 		 		   		 		  
        ax.set_xlabel("Date")  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_ylabel(attribute) 
        plt.savefig("../stats/" + player + "/"+ attribute +".png")
        plt.close()

def get_profiency(player, start_date, end_date):
    if not os.path.exists("../stats/" + player):
        os.mkdir("../stats/" + player)
    kind="line"
    if end_date is None:
        kind="bar"
        end_date = start_date
    
    df_summary = pd.read_csv("../data/master_summary.csv", index_col=[20, 0])
    df_box = pd.read_csv("../data/box_score_master.csv", index_col=[1,6])
    df_box.index = df_box.index.set_names('Player Name', level=1)
    df_box.index = df_box.index.set_names('date', level=0)
    # print(df_box)
    df_summary.index = df_summary.index.set_levels([pd.to_datetime(df_summary.index.levels[0]), df_summary.index.levels[1]])
    df_box.index = df_box.index.set_levels([pd.to_datetime(df_box.index.levels[0]), df_box.index.levels[1]])
    # print(df_summary)
    # merged = pd.merge(df_box.reset_index(),df_summary.reset_index(),on=['date','second'])
    # result = merged['0_x']*merged['0_y']
    # result.index = s1.index

    df_summary["Proficiency (Energy/attempt)"] = (df_summary["Kinetic Energy (Joules/Pound)"] / df_box["TA"])
    df_summary = df_summary.reset_index().set_index("date")[start_date : end_date]

    df_attribute_average = df_summary.groupby(['date', 'Player Name'])["Proficiency (Energy/attempt)"].mean().reset_index(name=player)
    player_attribute_data = df_attribute_average.loc[(df_attribute_average['Player Name'] == player)]
    del player_attribute_data['Player Name']
    player_attribute_data = player_attribute_data.set_index('date')
    player_attribute_data.index = player_attribute_data.index.date

    ax = player_attribute_data.plot(title="Proficiency", kind="bar")
    ax.set_xlabel("Date")  		   	  			    		  		  		    	 		 		   		 		  
    ax.set_ylabel("Proficiency (Energy/attempt)") 
    plt.savefig("../stats/" + player + "/Proficiency.png")
    plt.close()

if __name__ == "__main__":
    # get_summary_data("Team", "Kinetic Energy (Joules/Pound)",'10/01/2017', '11/28/2017')
    # get_box_data('Kodie Comby', 'K', '10/1/2017 0:00', '11/24/2017 0:00')
    # get_profiency('Cori Clifton', '10/20/2017', '11/28/2017')
    # get_jump_data("Gabby Benda", '10/01/2017', '11/28/2017')
    # get_summary_data("Kodie Comby", "Energy per Inched Jump",'10/01/2017', '11/28/2017')
    # get_impact_data('Kodie Comby', '10/1/2017', '11/24/2017')
    
    df_jump = pd.read_csv("../data/2017_GAMES_JUMP_MASTER.csv", index_col=1)
    players = set(df_jump['player name'].values)
    if not os.path.exists("../stats"):
        os.mkdir("../stats")
    for player in players:
        get_jump_data(player, '10/1/2017', '11/24/2017')
    df_impact = pd.read_csv("../data/2017_GAME_IMPACT_MASTER.csv", index_col=1)
    players = set(df_impact['player name'].values)
    for player in players:
        get_impact_data(player, '10/1/2017', '11/24/2017')
    df_summary = pd.read_csv("../data/master_summary.csv", index_col=1)
    players = set(df_summary['Player Name'].values)
    attributes = df_summary.columns.values
    for player in players:
        for attr in attributes:
            if attr not in ["date", "Player Name"]:
                get_summary_data(player, attr,'10/1/2017', '11/24/2017')
    
    
    

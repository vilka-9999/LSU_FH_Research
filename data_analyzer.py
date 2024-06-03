import csv
import numpy
import pandas
import matplotlib.pyplot as plt
import os

#############################
# functions for cleaning data
#############################

# adds Year column
def clean_data_year(df):
    years = []
    # fills "years list" where index is a year's number and the element at that index is an index of the table row
    # The index of a row is the last index of the row with the current year
    for i in range(len(df['Date']) - 1):
        if int(df['Date'][i+1]) - int(df['Date'][i]) > 50:
            years.append(i)
    years.append(len(df['Date']) - 1)
    # fills the table rows by checking if an index smaller than index of the the last row with the same year
    def YearSetup(row):
        for y in range(len(years)):
            if row.name <= years[y]:
                return int(y + 1)
    # insert Year column        
    df.insert(0, 'Year', 0)
    df['Year'] = df.apply(YearSetup, axis=1)
    

# adds WeekDay column
def clean_data_weekDay(df):
    # fills each row based on the remainder of the division 'Date' by 7
    def WeekDaySetup(row):
        if int(row['Date']) % 7 == 4:
            return '3 Wen'
        elif int(row['Date']) % 7 == 5:
            return '4 Thu'
        elif int(row['Date']) % 7 == 6:
            return '5 Fri'
        elif int(row['Date']) % 7 == 0:
            return '6 Sat'
        elif int(row['Date']) % 7 == 1:
            return '7 Sun'
        elif int(row['Date']) % 7 == 2:
            return '1 Mon'
        elif int(row['Date']) % 7 == 3:
            return '2 Tue'
    # insert WeekDay column
    df.insert(2, 'WeekDay', 0)
    df['WeekDay'] = df.apply(WeekDaySetup, axis=1)
    

# adds Week column
def clean_data_week(df):
    weeks = []
    # fills "weeks list" where index is a week's number and the element at that index is an index of the table row
    # The index of a row is the last index of the row with the current week
    for i in range(len(df['Date']) - 1):
        if int(df['WeekDay'][i+1][0]) - int(df['WeekDay'][i][0]) < 0:
            weeks.append(i)
        elif int(df['Year'][i+1]) != int(df['Year'][i]):
            weeks.append(i)
    weeks.append(len(df['Date']) - 1)
    # fills the table rows by checking if index smaller than index of the the last row with the same week
    def WeekSetup(row):
        for w in range(len(weeks)):
            if row.name <= weeks[w]:
                return int(w + 1)
    # insert Week column     
    df.insert(1, 'Week', 0)
    df['Week'] = df.apply(WeekSetup, axis=1)
    

# function groups all functions for cleaninf data 
def clean_data(df):
    try:
        # check if file already exists
        clean_df = pandas.read_csv('data_cleaned/clean_data.csv')
        print('clean_data.scv alredy exists')
    except:
        # create clean_data file if it does not exist
        clean_df = df.sort_values(['Date']).reset_index(drop=True)
        clean_data_year(clean_df)
        clean_data_weekDay(clean_df)
        clean_data_week(clean_df)
        # save  clean_data file
        os.makedirs('data_cleaned', exist_ok=True)
        clean_df.to_csv('data_cleaned/clean_data.csv', encoding='utf-8', index=False)
        print('clean_data.scv was created')
    return clean_df


#############################
# functions for splitting data
#############################


# spliting data bt provided tag
def split_by_tag(df, tag, folder_name, file_name):
    os.makedirs('data_cleaned/split_data', exist_ok=True) # create split data dirrectory
    try: 
        games_df = pandas.read_csv(f'data_cleaned/split_data/{folder_name}/{file_name}')
        print(f'{file_name} already exists')
    except:
        os.makedirs(f'data_cleaned/split_data/{folder_name}', exist_ok=True)
        games_df = df[df['Tags'] == f"{tag}"].reset_index(drop=True)
        games_df.to_csv(f'data_cleaned/split_data/{folder_name}/{file_name}', encoding='utf-8', index=False)
        print(f'{file_name} was created')


# functions groups all splitting functions
def split(df):

    split_by_tag(df, 'game', 'games', 'games.csv')
    split_by_tag(df, 'training', 'trainings', 'trainings.csv')
    split_by_tag(df, 'training game', 'trainings', 'training_games.csv')

    # other data splits for files created in this function


#############################
# functions for analyzing data
#############################    

# creates file for miles per week based on provided data and name
def miles_per_week(df, file_name):
    if os.path.exists(f'data_analyzed/miles_per_week/{file_name}'):
        print(f'{file_name} already exists')
    else:
        df_grouped = df.groupby(['Week', 'Player Name']).agg(Distance_per_week=('Distance (miles)', 'sum')).reset_index()
        df_pivoted = df_grouped.pivot(index='Week', columns='Player Name', values='Distance_per_week')
        df_pivoted.to_excel(f'data_analyzed/miles_per_week/{file_name}')
        print(f'{file_name} was created')


# functions groups all analyzing functions
def analyze():
    os.makedirs('data_analyzed', exist_ok=True)
    # main dfs to analyze
    clean_df = pandas.read_csv('data_cleaned/clean_data.csv')
    games_df = pandas.read_csv('data_cleaned/split_data/games/games.csv')
    trainings_df = pandas.read_csv('data_cleaned/split_data/trainings/trainings.csv')

    # miles per week for every file
    os.makedirs('data_analyzed/miles_per_week', exist_ok=True)
    miles_per_week(clean_df, 'miles_per_week_all_data.xlsx')
    miles_per_week(trainings_df, 'miles_per_week_trainings.xlsx')
    miles_per_week(games_df, 'miles_per_week_games.xlsx')



def main():
    data = pandas.read_csv('data/All Data as of 2024.05.30.csv') # load data
    clean_df = clean_data(data)
    split(clean_df)
    analyze()

if __name__ == "__main__":
    main()




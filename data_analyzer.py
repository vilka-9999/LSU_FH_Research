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
    def SemesterSetup(row):
        for y in range(len(years)):
            if row.name <= years[y]:
                return int(y + 1)
    # insert Year column        
    df.insert(0, 'Semester', 0)
    df['Semester'] = df.apply(SemesterSetup, axis=1)
    

# adds WeekDay column
def clean_data_weekDay(df):
    # fills each row based on the remainder of the division 'Date' by 7
    def WeekDaySetup(row):
        if int(row['Date']) % 7 == 4:
            return 3
        elif int(row['Date']) % 7 == 5:
            return 4
        elif int(row['Date']) % 7 == 6:
            return 5
        elif int(row['Date']) % 7 == 0:
            return 6
        elif int(row['Date']) % 7 == 1:
            return 7
        elif int(row['Date']) % 7 == 2:
            return 1
        elif int(row['Date']) % 7 == 3:
            return 2
    # insert WeekDay column
    df.insert(2, 'WeekDay', 0)
    df['WeekDay'] = df.apply(WeekDaySetup, axis=1)
    

# adds Week column
def clean_data_week(df):
    weeks = []
    # fills "weeks list" where index is a week's number and the element at that index is an index of the table row
    # The index of a row is the last index of the row with the current week
    for i in range(len(df['Date']) - 1):
        if int(df['WeekDay'][i+1]) - int(df['WeekDay'][i]) < 0:
            weeks.append(i)
        elif int(df['Semester'][i+1]) != int(df['Semester'][i]):
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
        df_splitted = pandas.read_csv(f'data_cleaned/split_data/{folder_name}/{file_name}')
        print(f'{file_name} already exists')
    except:
        os.makedirs(f'data_cleaned/split_data/{folder_name}', exist_ok=True)
        
        df_splitted.to_csv(f'data_cleaned/split_data/{folder_name}/{file_name}', encoding='utf-8', index=False)
        print(f'{file_name} was created')
    return df_splitted


# split games by split_name value
def split_games(df, split_name, file_name):
    if os.path.exists(f'data_cleaned/split_data/games/{file_name}'):
        print(f'{file_name} already exists')
        return
    
    games_splited = df[df['Split Name'].str.contains(f"{split_name}", regex=False, na=False)].reset_index(drop=True)
    games_splited.to_csv(f'data_cleaned/split_data/games/{file_name}', encoding='utf-8', index=False)
    print(f'{file_name} was created')
    

# split trainings by session value
def split_trainings(df, session, file_name):
    if os.path.exists(f'data_cleaned/split_data/trainings/{file_name}'):
        print(f'{file_name} already exists')
        return 

    games_splited = df[df['Session Title'].str.contains(f"{session}", regex=False, na=False)].reset_index(drop=True)
    games_splited.to_csv(f'data_cleaned/split_data/trainings/{file_name}', encoding='utf-8', index=False)
    print(f'{file_name} was created')


def split_by_semester(df):
    if os.path.exists(f'data_cleaned/split_data/semesters'):
        print(f'semesters already exists')
        return
    
    os.makedirs(f'data_cleaned/split_data/semesters', exist_ok=True)
    
    df = df[df['Split Name'] == "all"].reset_index(drop=True)
    df.to_csv(f'data_cleaned/split_data/semesters/all.csv', encoding='utf-8', index=False)

    semesters = df['Semester'].unique()
    spring = []
    fall = []
    for s in semesters:
        if s % 2 == 0:
            spring.append(s)
        else:
            fall.append(s)

    df_splitted = df[df['Semester'].isin(spring)].reset_index(drop=True)
    df_splitted.to_csv(f'data_cleaned/split_data/semesters/spring.csv', encoding='utf-8', index=False)
    print(f'spring.csv was created')
    df_splitted = df[df['Semester'].isin(fall)].reset_index(drop=True)
    df_splitted.to_csv(f'data_cleaned/split_data/semesters/fall.csv', encoding='utf-8', index=False)
    print(f'fall.csv was created')




# functions groups all splitting functions
def split(df):
    # main split
    games_df = split_by_tag(df, 'game', 'games', 'games.csv')
    trainings_df = split_by_tag(df, 'training', 'trainings', 'trainings.csv')
    split_by_semester(df)

    # split games df by game time
    split_games(games_df, 'all', 'games_all.csv')
    split_games(games_df, '1Q', 'games_1q.csv')
    split_games(games_df, '2Q', 'games_2q.csv')
    split_games(games_df, '3Q', 'games_3q.csv')
    split_games(games_df, '4Q', 'games_4q.csv')
    split_games(games_df, 'warmups', 'games_warmup.csv')

    # split trainings
    split_trainings(trainings_df, 'Practice', 'trainings_practice.csv',)
    split_trainings(trainings_df, 'Conditioning', 'trainings_conditioning.csv',)
    split_trainings(trainings_df, 'Pre-game', 'trainings_pregame.csv',)


#############################
# functions for analyzing data
#############################    

# creates file for miles per week based on provided data and name
def miles_per_week(df, file_name):
    if os.path.exists(f'data_analyzed/miles_per_week/{file_name}'):
        print(f'{file_name} already exists')
        return

    df_grouped = df.groupby(['Week', 'Player Name']).agg(Distance_per_week=('Distance (miles)', 'sum')).reset_index()
    df_pivoted = df_grouped.pivot(index='Week', columns='Player Name', values='Distance_per_week')
    df_pivoted.to_excel(f'data_analyzed/miles_per_week/{file_name}')
    print(f'{file_name} was created')


# creates xlsx files based on value to analyze
def table_value_analysis(df, value, filename):
    # replace / since it would create directory
    folder = value.replace('/', '-')
    filename = filename.replace('/', '-')
    filename = f'{folder}_{filename}.csv'

    if os.path.exists(f'data_analyzed/{folder}/{filename}'):
        print(f'{filename} already exists')
        return
    
    os.makedirs(f'data_analyzed/{folder}', exist_ok=True)
    df_grouped = df.groupby(['Date', 'Player Name']).agg(values=(f'{value}', 'max')).reset_index()
    df_pivoted = df_grouped.pivot(index='Date', columns='Player Name', values='values')
    df_pivoted.to_csv(f'data_analyzed/{folder}/{filename}')
    print(f'{filename} was created')

    
# functions groups all analyzing functions
def analyze():
    os.makedirs('data_analyzed', exist_ok=True)
    # main dfs to analyze
    clean_df = pandas.read_csv('data_cleaned/clean_data.csv')
    clean_df = clean_df[clean_df['Split Name'] == "all"].reset_index(drop=True)
    games_df = pandas.read_csv('data_cleaned/split_data/games/games.csv')
    games_df = games_df[games_df['Split Name'] == "all"].reset_index(drop=True)
    trainings_df = pandas.read_csv('data_cleaned/split_data/trainings/trainings.csv')

    # miles per week for every file
    os.makedirs('data_analyzed/miles_per_week', exist_ok=True)
    miles_per_week(clean_df, 'miles_per_week_all_data.xlsx')
    miles_per_week(trainings_df, 'miles_per_week_trainings.xlsx')
    miles_per_week(games_df, 'miles_per_week_games.xlsx')

    # analyzing split data
    for dirpath, dirnames, filenames in os.walk('data_cleaned/split_data'):
        for filename in filenames:
            # set up
            file_path = os.path.join(dirpath, filename)
            file = pandas.read_csv(file_path)
            filename = filename[:filename.index('.')]
            # analysis
            table_value_analysis(file, 'Distance (miles)', filename)
            table_value_analysis(file, 'Energy (kcal)', filename)
            table_value_analysis(file, 'Top Speed (m/s)', filename)
            table_value_analysis(file, 'Power Score (w/kg)', filename)
            table_value_analysis(file, 'Work Ratio', filename)
            table_value_analysis(file, 'Duration', filename)
            table_value_analysis(file, 'Distance Per Min (m/min)', filename)
                                        
            

def main():
    data = pandas.read_csv('data/All Data as of 2024.05.30 (normalized).csv') # load data
    clean_df = clean_data(data)
    split(clean_df)
    analyze()

if __name__ == "__main__":
    main()




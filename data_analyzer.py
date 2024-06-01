import csv
import numpy
import pandas
import matplotlib.pyplot as plt


def clean_data(df):
    # Sort by column: 'Date' (ascending)
    df = df.sort_values(['Date']).reset_index(drop=True)
    # Derive column 'Year' from column: 'Date'
    def YearSetup(row):
        years = []
        for i in range(len(df['Date']) - 1):
            if int(df['Date'][i+1]) - int(df['Date'][i]) > 50:
                years.append(i)
        years.append(len(df['Date']) - 1)
        for y in range(len(years)):
            if row.name < years[y]:
                return int(y + 1)
    df.insert(0, 'Year', 0)
    df['Year'] = df.apply(YearSetup, axis=1)
    return df


def avg_dist(data):
    # Performed 1 aggregation grouped on column: 'Player Name'
    # avg distance for player per week for all players
    df = data.groupby(['Player Name', 'WeekDays']).agg(Distancekm_avg=('Distance (km)', 'mean')).reset_index()
    df_excel = df.pivot(index='Player Name', columns='WeekDays', values='Distancekm_avg')
    print(df_excel)
    # df.to_excel('output.xlsx', index=True)

def main():
    # load data
    data = pandas.read_csv('data/All Data as of 2024.05.03 csv.csv')
    avg_dist(data)
    

if __name__ == "__main__":
    main()




import csv
import numpy
import pandas
import matplotlib.pyplot as plt

def clean_data_year(df):
    years = []
    for i in range(len(df['Date']) - 1):
        if int(df['Date'][i+1]) - int(df['Date'][i]) > 50:
            years.append(i)
    years.append(len(df['Date']) - 1)
    def YearSetup(row):
        for y in range(len(years)):
            if row.name <= years[y]:
                return int(y + 1)
    df.insert(0, 'Year', 0)
    df['Year'] = df.apply(YearSetup, axis=1)
    return df

def clean_data_weekDay(df):
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
    df.insert(2, 'WeekDay', 0)
    df['WeekDay'] = df.apply(WeekDaySetup, axis=1)
    return df

def clean_data_week(df):
    weeks = []
    for i in range(len(df['Date']) - 1):
        if int(df['WeekDay'][i+1][0]) - int(df['WeekDay'][i][0]) < 0:
            weeks.append(i)
        elif int(df['Year'][i+1]) != int(df['Year'][i]):
            weeks.append(i)
    weeks.append(i)

    def WeekSetup(row):
        for w in range(len(weeks)):
            if row.name <= weeks[w]:
                return int(w + 1)
        
    df.insert(1, 'Week', 0)
    df['Week'] = df.apply(WeekSetup, axis=1)
    return df

def clean_data(df):
    df = df.sort_values(['Date']).reset_index(drop=True)
    df = clean_data_year(df)
    df = clean_data_weekDay(df)
    df = clean_data_week(df)
    return df


def main():
    # load data
    data = pandas.read_csv('data\All Data as of 2024.05.30 csv.csv')
    clean_df = clean_data(data)
    #clean_df.to_csv('data_cleaned/clean_data.csv', encoding='utf-8', index=False) # save cleaned data to scv
    

if __name__ == "__main__":
    main()




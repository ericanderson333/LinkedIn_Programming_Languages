import pandas as pd
from sklearn import preprocessing

def menu():
    c = -1
    while c != 0 and c != 1 and c != 2 and c != 3:
        print('\nCHOSE OPTION BELOW:')
        print("\n'0' - Quit")
        print("\n'1' - Display all jobs and their top 3 programming languages")
        print("\n'2' - Search by job title and display their programming languages")
        print("\n'3' - Search by programming language and show their respective top jobs")
        c = int(input("\nEnter here: "))

    return c
def display_all(df, job_names, count_df):
    #create df into all percentages
    percent_df = ((100 * df) / (df.sum(axis=0))).round(1)
    #iterate through each column
    for name in job_names:
        top_three = percent_df.nlargest(3, [name])
        top_three = top_three.astype(str) + '%'
        print(" ")
        print(name + ': Out of', count_df[name]['COUNT'], 'jobs: ')
        for rows in top_three[name].index:
            print(rows, ':', top_three[name][rows])


def by_job(choice, data_df, count_df):
    percent_df = ((100 * data_df) / (data_df.sum(axis=0))).round(1)
    for i, name in enumerate(data_df.columns):
        if i == choice:
            print(" ")
            print(name + ': Out of', count_df[name]['COUNT'], 'jobs: ')
            for rows in percent_df[name].index:
                if percent_df[name][rows] != 0:
                    print(rows, ':', percent_df[name][rows].astype(str) + '%')
def by_lang(choice, data_df, lang_names, job_names):
    #scale data for each row (programming language)
    x = data_df.values
    scaler = preprocessing.MinMaxScaler()
    scaled_data = scaler.fit_transform(x)
    data_df = pd.DataFrame(scaled_data)
    #set percentages for each row
    for name in data_df.index:
        data_df.loc[name] = ((data_df.loc[name] * 100) / (data_df.loc[name].sum(axis=0))).round(1)
    data_df = data_df.dropna(0)

    try:
        for i, name in enumerate(lang_names):
            if i == choice:
                print(" ")
                print(name + ':')
                for col, job in enumerate(job_names):
                    #if data_df.loc[col][i] != 0:
                    print(job, ':', data_df[col][i].astype(str) + '%')
    except KeyError:
        print("No values")



#console project
if __name__ == '__main__':
    #get data from previous file, then configure columns.
    data_df = pd.read_csv('data/merged_job_lang_data.csv')
    count_df = pd.read_csv('data/merged_job_count_data.csv')

    #configure for data
    data_df.rename(columns={'Unnamed: 0.1': 'Prog Langs'}, inplace=True)
    data_df.drop(data_df.columns[data_df.columns.str.contains('Unnamed: 0', case=False)], axis=1, inplace=True)
    Rows = data_df['Prog Langs']
    data_df.drop(['Prog Langs'], axis=1 ,inplace=True)
    data_df.index = Rows

    #configure for count
    count_df.rename(columns={'Unnamed: 0.1': 'VAR'}, inplace=True)
    count_df.drop(count_df.columns[count_df.columns.str.contains('Unnamed: 0', case=False)], axis=1, inplace=True)
    countRows = count_df['VAR']
    count_df.drop(['VAR'], axis=1, inplace=True)
    count_df.index = countRows

    #drop 'R' language, this is because there is error that is noted in getting data
    data_df.drop(['R'], axis=0, inplace=True)

    #Get array of column names and row names to travser through later
    job_names = data_df.columns
    lang_names = data_df.index


    #main menu portion
    choice = -1
    while choice != 0:
        choice = menu()
        if choice == 1:
            display_all(data_df, job_names) 
        elif choice == 2:
            print("\nList of job titles, select by number")
            for i, item in enumerate(job_names):
                print("'", i, "' - for", item)
            user_choice = int(input('Enter Here: '))
            #pass through
            by_job(user_choice, data_df, count_df)
        elif choice == 3:
            print("\nList of programming languages, select by number")
            for i, item in enumerate(lang_names):
                print("'", i, "' - for", item)
            user_choice = int(input('Enter Here: '))
            #pass through
            by_lang(user_choice, data_df, lang_names, job_names)










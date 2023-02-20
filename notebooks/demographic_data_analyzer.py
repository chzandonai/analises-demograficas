import pandas as pd
import urllib


def calculate_demographic_data(print_data=True):
    # Read data from file
    url_data = 'https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data'
    url_names = 'https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.names'
    url_test = 'https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test'
    def importa_salva_dados(url,filename,pasta='../src/data/'):
        resposta = requests.get(url)
        urllib.request.urlretrieve(url,filename=pasta+filename)
    mporta_salva_dados(url_data,'adult_data.csv')
    importa_salva_dados(url_names,'adult_names.csv')
    importa_salva_dados(url_test,'adult_test.csv')
    with open('../src/data/adult_names.csv', 'r') as file: lines = file.read().split('\n')
    lines_ = [line.split(': ') for line in lines[-15:]]
    headers = [head[0] for head in lines_[:]]
    headers[-1] = 'target'
    data = pd.read_csv('../src/data/adult_data.csv',header = None, delimiter=(', '))
    data.columns = headers
      
    # df = pd.read_csv('adult.data.csv')
        
    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    group_race = data.groupby('race').count()['target']
    data_race_count = pd.DataFrame(group_race)
    data_race_count.columns = ['race_count']
    race_count = data.groupby('race').count()['target'].tolist()

    # What is the average age of men?
    average_age_men = data.groupby('sex').mean()['age'][1]

    # What is the percentage of people who have a Bachelor's degree?
    tot_bach = data[data.education == 'Bachelors'].count()[0]
    non_bach = data[data.education != 'Bachelors'].count()[0]
    percentage_bachelors = tot_bach/(non_bach+tot_bach)*100

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    
#     higher_education = None
#     lower_education = None

    # percentage with salary >50K
    group_edu_salary = data.loc[((data.education == 'Bachelors')|(data.education == 'Doctorate')|(data.education == 'Masters')), 
         ['education','target']].groupby('target').count()
    higher_education_rich = 100*group_edu_salary['education'][1]/(group_edu_salary['education'][1]+group_edu_salary['education'][0])
    group_no_edu_salary = data.loc[((data.education != 'Bachelors')
                                &(data.education != 'Doctorate')
                                &(data.education != 'Masters')),['education','target']].groupby('target').count()
    lower_education_rich = 100*group_no_edu_salary['education'][1]/(group_no_edu_salary['education'][1]+group_no_edu_salary['education'][0])

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = data['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_minh_50gain = data.loc[((data['hours-per-week'] == 1) & (data.target == '>50K')),['target']].count()[0]
    num_no_minh_50gain = data.loc[(((data['hours-per-week'] == 1) & (data.target != '>50K'))),['target']].count()[0]
    rich_percentage = 100*num_minh_50gain/(num_minh_50gain+num_no_minh_50gain)

    # What country has the highest percentage of people that earn >50K?
    A = pd.DataFrame(data.loc[data.target == '>50K'].groupby('native-country').count().target)
    A['target_low'] = pd.DataFrame(data.loc[data.target != '>50K'].groupby('native-country').count().target).target
    A['total'] = A.target+A.target_low
    A['perc_high'] = A.target/A.total*100
    A = A.sort_values('perc_high', ascending=False)
    highest_earning_country = A.index[0]
    highest_earning_country_percentage = A.perc_high[0]
    
    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = data.loc[((data['native-country']=='India')
                                &(data.target=='>50K')),['occupation',
                                'target']].groupby('occupation').count().sort_values('target',
                                ascending=False).index[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

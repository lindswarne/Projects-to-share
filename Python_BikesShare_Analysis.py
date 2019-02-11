import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
        if city in ('chicago', 'new york city', 'washington'):
             break
        else:
             print('Sorry, we don\'t have data for that city. Please try Chicago, New York or Washington.')
    print(city)
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Would you like to see data for January, February, March, April, May or June?\n').lower()
        if month in ('january', 'february', 'march', 'april', 'may', 'june'):
             break
        else:
             print('Sorry, we don\'t have data for that month. Please try a month from January to June.')
        print(month)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Would you like to see data for Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?\n').lower()
        if day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
             break
        else:
             print('Sorry, we that\'s not a valid day value. Please try a day of the week.')
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # read city data from CITY_DATA
    df = pd.read_csv(CITY_DATA[city])
    city = city.lower()
    if city == 'Chicago':
    	return 'chicago.csv'
    elif city == 'New York':
    	return 'new_york_city.csv'
    elif city == 'Washington':
    	return 'washington.csv'
    
    # get month filter
    # convert the Start Time column to datetime
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
       months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
       month = months.index(month) + 1
        # filter by month to create the new dataframe
    df = df[df['month'] == month]
   
    #  filter by day if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day.title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    #extract month from Start Time and create a month column
    df['month'] = df['Start Time'].dt.month
    #find most common months
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # extract day from Start Time and create day column
    df['day'] = df['Start Time'].dt.weekday_name
    #find most common day of week
    day_list =  df['day'].value_counts().index.tolist()
    popular_day = str(day_list[0])
    print('Most Popular Day of Week:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    # find most common hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Hour of Day:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()
    print('Most Popular Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    #group by start and end station columns, use size to get number of elements and then store in groupby_size
    groupby_size = df.groupby(['Start Station', 'End Station']).size().reset_index(name='groupby_size')
    sort = groupby_size.sort_values(by='groupby_size',ascending=False).drop_duplicates(['Start Station', 'End Station'])
    start = sort['Start Station'].iloc[0]
    end = sort['End Station'].iloc[0]
    print('Most Frequent Combination of Start and End Stations:', start, end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Time Travel(seconds):', total_travel_time)
  
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Time Travel(seconds):', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def user_stats(df):
    """Displays statistics on bikeshare users.""" 
    print('\nCalculating User Stats...\n')
    start_time = time.time()   
    # Display counts of user types
    # print value counts for each user type
    user_types = df['User Type'].value_counts()
    print('Subscribers and Customers', user_types)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def gender_stats(df):
    print('\nCalculating Gender Stats...\n')
    try:
        gender_count = df['Gender'].value_counts()
        print('Counts of Men and Women:', gender_count)
    except KeyError:
        print('Sorry, there is no gender data for Washington.')  
   
    # Display earliest, most recent, and most common year of birth
def birth_stats(df):
    print('\nCalculating Birth Year Stats...\n')
    try:
        earliest_year = df['Birth Year'].min()
        print('Earliest Birth Year:',earliest_year)
    except KeyError:
        print("\nCannot find earliest birth year. There is no Birth Year data for Washington")
	
    try:
        most_recentyear = df['Birth Year'].max()
        print('Latest Birth Year:',most_recentyear)
    except KeyError:
        print("\nCannot find latest birth year. There is no Birth Year data for Washington") 

    try:
        common_year = df['Birth Year'].mode()
        print('Most Common Birth Year:',common_year) 
    except KeyError:
        print("\nCannot find most common birth year. There is no Birth Year data for Washington")     
def display_data(city):
    trip_data = input('Would you like to view the table of trip data? Type yes or no.\n')
    x=0
    y=5
    if trip_data == 'yes':
        print(city.iloc[x:y])
        while x < len(city.index):
            display = input('Would you like to view the next 5 lines of data? Type yes or no.\n')
            if display == 'yes':
                x = x + 5
                y = y + 5
                print(city.iloc[x:y])
            else:
                print('No problem, thanks!')
                break
                	
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        gender_stats(df)
        birth_stats(df)
        display_data(df)

        
        
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()






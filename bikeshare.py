import time
import calendar
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
    city = ''
    while True:
        city = input('For which city would you like to see data? The options are Chicago, New York City, and Washington.\n').lower()
        if city in ['nyc', 'new york']: #"NYC" is an abbreviation for New York City.
            city = 'new york city'
        if city in ['chicago', 'new york city', 'washington']:
            break
        print("I don't have data on that city.\n")

    month = ''
    while True:
        month = input('For which month would you like to see data? The options are all (to see data from all available months), January, February, ..., June.\n').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        print("I don't have data for that month.\n")

    day = ''
    while True:
        day = input('For which day of the week would you like to see data? Enter a day of the week or "all" to see data for all days of the week.\n').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        print("That isn't a valid response.\n")

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
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        #print(df)
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    #print(df)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    month_mode = calendar.month_name[df['month'].mode()[0]]
    print(f"The most common month to travel is {month_mode}.")

    day_mode = df['day_of_week'].mode()[0]
    print(f"The most common day of the week to travel is {day_mode}.")

    hour_mode = df['Start Time'].dt.strftime('%I %p').mode()[0]
    print(f"The most common hour to start a trip is {hour_mode}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start_station_mode = df['Start Station'].mode()[0]
    print(f"The most commononly used start station is {start_station_mode}.")

    end_station_mode = df['End Station'].mode()[0]
    print(f"The most commononly used end station is {end_station_mode}.")

    trip_stations_mode = ("Start Station: " + df['Start Station'] + "\nEnd Station: " + df['End Station']).mode()[0]
    print(f"The most frequent combination of start station and end station for a trip is:\n{trip_stations_mode}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_time = df['Trip Duration'].sum()
    print(f'The total travel time is {total_time} seconds.')

    average_time = df['Trip Duration'].mean()
    print(f'The average travel time is {average_time} seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_counts = df['User Type'].value_counts()
    print('Here are how many of each user type:')
    print(user_counts.to_string(dtype=False))
    
    try:
        gender_counts = df['Gender'].value_counts()
        print('\nHere are how many of each gender:')
        print(gender_counts.to_string(dtype=False))
    except:
        pass

    try:
        earliest_year = int(df['Birth Year'].min())
        print(f'\nEarliest year of birth: {earliest_year}')
    
        latest_year = int(df['Birth Year'].max())
        print(f'Most recent year of birth: {latest_year}')
    
        year_mode = int(df['Birth Year'].mode()[0])
        print(f'Most common year of birth: {year_mode}')
    except:
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """ Repeatedly asks user if they would like to see 5 lines of the raw data and displays the next 5 lines until user enters 'n' or 'no' or there is no more data to display."""
    row = 0
    while row < len(df):
        see_raw = input('\nWould you like to see 5 lines of the raw data?\n').lower()
        if see_raw in ['y', 'yes']:
            print(df.iloc[row:row+5])
            row += 5
        elif see_raw in ['n', 'no']:
            break
        else:
            print('That is not a valid response.')
    if row >= len(df):
        print('You have reached the end of the data.')
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        raw_data(df)
        
        restart = input('\nWould you like to restart?\n')
        if restart.lower() not in ['y', 'yes']:
            break


if __name__ == "__main__":
	main()

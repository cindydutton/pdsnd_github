import time
import numpy as np
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a name, city, month, and day to analyze.

    Returns:
        (str) name - name of user
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # Get user name for personalised greeting
    # Useful article: https://www.askpython.com/python/examples/python-user-input#:~:text=Python%20User%20Input%20from%20Keyboard%20%E2%80%93%20input%20%28%29,for%20the%20user%20input.%20...%20More%20items...%20
    name = input("Hello! Let's explore some US Bikeshare data! Can I please start with your name?\n").lower()
    print("Welcome, {}! Let's begin!".format(name.title()))

    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']

    while True:
        city = input("\nWhich city would you like to select?\nChicago\nNew York City\nWashington?\n").lower()
        if city not in cities:
            print("Sorry, input is invalid. Please try again.\n")
            continue
        else:
            break

    # Get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

    while True:
        month = input("\nWhich month would you like to select?\nJanuary\nFebruary\nMarch\nApril\nMay\nJune\nAll\n").lower()
        if month not in months:
            print("Sorry, input is invalid. Please try again.\n")
            continue
        else:
            break

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

    while True:
        day = input ("\nWhich day would you like to select?\nMonday\nTuesday\nWednesday\nThursday\nFriday\nSaturday\nSunday\nAll\n").lower()
        if day not in days:
            print("Sorry, input is invalid. Please try again.\n")
            continue
        else:
            break

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

    df = pd.read_csv("{}.csv".format(city.replace(" ","_")))

    # Convert the Start and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Extract month and day of week from Start Time to create new columns
    # Useful article: https://towardsdatascience.com/mastering-dates-and-timestamps-in-pandas-and-python-in-general-5b8c6edcc50c
    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['day_of_week'] = df['Start Time'].apply(lambda x: x.strftime('%A').lower())

    # Filter by month if applicable
    if month != 'all':

    # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    # filter by month to create the new dataframe
    # Useful article: https://towardsdatascience.com/how-to-use-loc-and-iloc-for-selecting-data-in-pandas-bd09cb4c3d79
        df = df.loc[df['month'] == month,:]

    # filter by day of week if applicable
    if day != 'all':

    # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day,:]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # Useful article: https://community.dataquest.io/t/why-mode-0-not-just-mode/5057
    # Useful article: https://www.w3resource.com/pandas/dataframe/dataframe-mode.php
    p_month = str(df['month'].mode().values[0])
    print("The most popular month is {}".format(p_month))

    # display the most common day of week
    p_day = str(df['day_of_week'].mode().values[0])
    print("The most popular day of the week is {}".format(p_day))

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    pstart_hour = str(df['start_hour'].mode().values[0])
    print("The most popular start hour is {}".format(pstart_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip"""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pstart_station = df['Start Station'].mode().values[0]
    print("The most popular start station is {}".format(pstart_station))

    # display most commonly used end station
    pend_station = df['End Station'].mode().values[0]
    print("The most popular end station is {}".format(pend_station))

    # display most frequent combination of start station and end station trip
    df['station_combo'] = df['Start Station'] + " " + ['End Station']
    p_trip = df['station_combo'].mode().values[0]
    print("The most popular trip is {}".format(p_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Trip Duration'] = df['End Time'] - df['Start Time']

    # display total travel time
    tot_travel_time = str(df['Trip Duration'].sum())
    print("The total travel time is {}".format(tot_travel_time))

    # display mean travel time
    mean_travel_time = str(df['Trip Duration'].mean())
    print("The mean travel time is {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = str(df['User Type'].value_counts())
    print("The user types are:\n", user_count)

    # Display counts of gender
    if('Gender' in df):
        gender_count = df['Gender'].value_counts()
        print("The counts of each gender are:\n", gender_count)
    else:
        print('Sorry! Gender data unavailable for Washington')

    # Display earliest, most recent, and most common year of birth
    if('Birth Year' in df):
        min_year = str(int(df['Birth Year'].min()))
        print("\nThe oldest user is born of the year", min_year)

        max_year = (int(df['Birth Year'].max()))
        print("The youngest user is born of the year", max_year)

        common_year = str(int(df['Birth Year'].mode().values[0]))
        print("Most users are born of the year", common_year)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def display_data(df):
    """Displays 5 lines of raw data depending on user's choice"""

    # Ask user to choose whether they would like to view 5 lines of raw data
    # Useful article: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.head.html
    # Useful article: https://www.freecodecamp.org/news/python-lowercase-how-to-use-the-string-lower-function/
    i = 1
    while True:
        option = input("\nWould you like to view 5 lines of raw data?\nYes\nNo\n").lower()
        if option == "yes":
            print(df[i:i+5])

            i = 1+5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input("\nWould you like to restart?\nYes\nNo\n")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

# use Numpy to do the simulation
# calculate profit = revenue-cost = room price * real booked room number - room cost -shuttle cost
import sympy
import numpy as np
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# "DAY" describes the time span, which is the time period that we calculate profit for.
DAY=300

# create a class for hotel, have distance attribute, roomNum attribute, guestType attribute, price attribute
class Hotel:
    """
    This class is about the hotel that we are going to construct. We define this class to generate random values of variables which are relevent to hotels
    It includes five attributes:
    :param distance: the distance between this hotel and the center of New York City (in miles)
    :param roomNum: the number of rooms that this hotel will have
    :param guestType: the probability distribution of the guest types, which includes solo and business travellers (mostly one person per room), couple and friend travellers （mostly two persons per room) and family travellers (mostly three persons per room)
                      we refer to the dataset on https://www.kaggle.com/crawford/las-vegas-tripadvisor-reviews, you can see more details in Reference_guesttype in Github.
    :param priceSeed: the lowest price that used to generated the LowPriceInterval, MediumPriceInterval and HighPriceInterval
                      we refer to the dataset on https://www.kaggle.com/gdberrio/new-york-hotels, you can see more details in Reference_price_new_york_hotels.csv (column: "low rate") in Github.
    :param price: the sum of the price in the time period
    """

    __distance=np.random.uniform(0, 30, 1) # (0,30] miles---- refer to Google Map
    __roomNum=np.random.random_integers(50, 2000, 1) # refer to Ctrip website
    __guestType=(0.19, 0.59, 0.22) # 19% solo & business travelers, 59% couple & friend travelers, 22% family travelers
    __priceSeed=np.random.randint(50, 1000, 1) # a randomly generated number from interval [50,1000]
    __price=0 # the initialized price value of hotel

    def getRoomNum(self):
        return self.__roomNum
    def getDistance(self):
        return self.__distance
    def getGuestType(self):
        return self.__guestType
    def getPrice(self):
        """
        This function is to generate random values of price.
        To better simulate price fluctuations over time, we divided the price into three continuous interval according to the price level, which are "LowPriceInterval", "MediumPriceInterval", "HighPriceInterval".
        It is known that the change of the hotel price has a fixed pattern. We could generate the hotel prices following that fixed pattern by finding out the probability distribution of the price intervals.

        :param LowPriceInterval: the low price range of this hotel, the left and right borders are 1 and 1.5 times of the "priceSeed" seperately
        :param MediumPriceInterval: the low price range of this hotel, the left and right borders are 1.5 and 2 times of the "priceSeed" seperately
        :param HighPriceInterval: the low price range of this hotel, the left and right borders are 2 and 2.5 times of the "priceSeed" seperately
                                all the multiples are obtained from the dataset 'new_york_hotels.csv'.(https://www.kaggle.com/gdberrio/new-york-hotels)
        :param DayRandom: the probability distribution of three price intervals, which means how many days the hotel prices will fall in the low price interval or medium price interval or high price interval
                          it is used to simulate the price change pattern in a certain time period
                          we analyzed the dataset on https://www.kaggle.com/airbnb/seattle#calendar.csv and the values of the probability are obtained based on the plots and analysis results.
                          you can see more details in Reference_price_pricechange
        :param lowPrice: a random price value generated from the LowPriceInterval
        :param mediumPrice: a random price value generated from the MediumPriceInterval
        :param highPrice: a random price value generated from the HighPriceInterval

        :return: a random total price in a certain time period
        """

        LowPriceInterval = (self.__priceSeed, self.__priceSeed * 1.5)  # reference: https://www.kaggle.com/gdberrio/new-york-hotels
        MediumPriceInterval = (self.__priceSeed * 1.5, self.__priceSeed * 2)
        HighPriceInterval = (self.__priceSeed * 2, self.__priceSeed * 2.5)
        DayRandom = (0.25, 0.5, 0.25)  # reference: https://www.kaggle.com/airbnb/seattle#calendar.csv
        # Generate a random value from the above intervals separately.
        lowPrice = np.random.random_integers(LowPriceInterval[0], LowPriceInterval[1], 1)  # From LowPriceInterval
        mediumPrice = np.random.random_integers(MediumPriceInterval[0], MediumPriceInterval[1], 1)  # From MediumPriceInterval
        highPrice = np.random.random_integers(HighPriceInterval[0], HighPriceInterval[1], 1)  # From HighPriceInterval
        self.__price = (lowPrice * DayRandom[0] + mediumPrice * DayRandom[1] + highPrice * DayRandom[2]) * DAY
        return self.__price


# create a class for shuttle, have cost attribute and shuttleFrequency attribute
class Shuttle:
    """
    We define shuttle class to generate random value of variables relevant to shuttle service.
    :param dayCost- how much shuttle service will cost per day.
                    To define its value, we refer to this website http://www.freightmetrics.com.au/Calculators%7CRoad/BusOperatingCost/tabid/671/Default.aspx
                    We modify some parameters, like the type of bus and average passengers, to get the suitable cost.
                    You can see more details in Reference_shuttlecost file in Github.
    :param cost- The total cost of shuttle service for certain days
    :param shuttleFrequency-how many days the hotel will provide shuttle service within given days
                            Since shuttle service is a random variable and have only two choices, it satisfy with binomial distribution.
    """
    __dayCost=790 # every day bus cost, reference----http://www.freightmetrics.com.au/Calculators%7CRoad/BusOperatingCost/tabid/671/Default.aspx
    __cost=0
    __shuttleFrequency=np.random.binomial(DAY,0.5,1) # shuttle is binomial

    def getCost(self):
        self.__cost=self.__dayCost*self.__shuttleFrequency
        return self.__cost

    def getFrequency(self):
        return self.__shuttleFrequency


# *location
# suppose the guest number have linear negative relationship with distance
# Guest number of a certain hotel, suppose the guest number have linear negative relationship with distance

def getGuestNum(hotel:Hotel,shuttle:Shuttle)->int:
    """
    This function is to get the real guest number considering the location impact and the shuttle service impact.

    Overall air passengers:
    We know the overall air passengers arrived at New York's five airports based on Kaggle dataset-
    -https://www.kaggle.com/new-york-state/nys-air-passenger-traffic,-port-authority-of-ny-nj. You can see more
    details in Reference_airpassenger file in Github.

    Guests of hotel without shuttle:
    In our simulation model, we suppose that distance will influence the guest number of a certain hotel.
    The farther away the hotel is from New York city center, the less guest it can get. Therefore, we define
    a negative linear relationship between variable GuestRate and variable distance, which means when the hotel
    is n miles closer to the city center, k*n percent of overall tourists they can get.(k is the slope)
    We get the highest guest rate and lowest guest rate from the number of reviews on TripAdvisor. You can see
    more details in reference_guestrate file in Github.

    Guests brought by shuttle:
    Since shuttle service will bring more guests for the hotel, we need to consider its influence.
    We suppose 20-seats-shuttle will go 5 round a day, so the additional guest number per day is 100.
    Real Guest of hotel= Guests of hotel without shuttle + Guests brought by shuttle

    :param hotel: Hotel object, which represents a new hotel model in our simulation
    :param shuttle: Shuttle object, which represents a new shuttle model in our simulation
    :return: calculated guest number of a certain hotel, which will be used to calculate the hotel revenue

    >>> getGuestNum(1,1)
    Traceback (most recent call last):
    TypeError: Parameters need to be hotel model and shuttle model.
    """

    # Determine whether the parameters are correct
    if not isinstance(hotel, Hotel) or not isinstance(shuttle, Shuttle):
        raise TypeError('Parameters need to be hotel model and shuttle model.')
    distance=hotel.getDistance()
    frequency=shuttle.getFrequency()
    # the number of air passenger per month
    GuestInterval=(7000000,11000000) # [7478511,11444185]  it is a uniform distribution-----https://www.kaggle.com/new-york-state/nys-air-passenger-traffic,-port-authority-of-ny-nj
    TotalGuestNum=np.random.random_integers(GuestInterval[0],GuestInterval[1],1)
    HighestGuestRate=0.00018   # we calculate the rate by "number of reviews*rate of people post reviews/number of guest"
    LowestGuestRate=HighestGuestRate/2.5  # reference from TripAdvisor number of reviews
    k=(HighestGuestRate-LowestGuestRate)/30.0 # the range of variable distance is from 0 to 30 miles
    locationInfluence=HighestGuestRate-k*distance # we suppose a negative linear relationship
    # since shuttle will bring more guests for hotels, we need to calculate its influence per day
    # 20 seat shuttle, go 5 round per day
    plusGuest = 100 * frequency  # this can be improved by random generating shuttle seats
    # plusGuest = shuttlePlusGuest * frequency
    # Real Guest Number = Guests of hotel without shuttle + Guests brought by shuttle
    hotelGuestNum=TotalGuestNum*locationInfluence+plusGuest
    return hotelGuestNum


def getBookedRoom(hotel:Hotel,shuttle:Shuttle)->int:
    """
    This function is to get the real booked room number according to the number of air passenger and the probability distribution of the guests.
    The guests are usually divided into three categories by the number of tourists travelling together, including single traveler, couple traveler and family traveler.
    With the guestType (obtained from https://www.kaggle.com/crawford/las-vegas-tripadvisor-reviews) and the GuestNum （calculated by the function getGuestNum), the real booked room number could be calculated by solving the equations.

    :param hotel: Hotel object, which represents a new hotel model in our simulation
    :param shuttle: Shuttle object, which represents a new shuttle model in our simulation
    :return: the real booked number of a certain hotel

    >>> getBookedRoom(1,1)
    Traceback (most recent call last):
    TypeError: Parameters need to be hotel model and shuttle model.
    """

    # Determine whether the parameters are correct
    if not isinstance(hotel, Hotel) or not isinstance(shuttle, Shuttle):
        raise TypeError('Parameters need to be hotel model and shuttle model.')

    # Solve ternary linear equations
    # x represents the booked number of single room, y represents the booked number of double room or twin room, z represents the booked number of triple room
    # Symbolize variables
    x = sympy.Symbol('x') # the booked number of single room
    y = sympy.Symbol('y') # the booked number of double room or twin room
    z = sympy.Symbol('z') # the booked number of triple room
    guestType=hotel.getGuestType()
    hotelGuestNum = getGuestNum(hotel,shuttle)
    # hotelGuestNum = x + 2y + 3z
    # 0.59x = 0.19y
    # 0.22x = 0.19z
    f1 = x + 2 * y + 3 * z - hotelGuestNum
    f2 = guestType[1] * x - guestType[0] * y
    f3 = guestType[2] * x - guestType[0] * z
    result = sympy.solve([f1, f2, f3], [x, y, z])
    # the real booked room number equals to the sum of the numbers of three types of rooms
    realBookedRoom = int(result[x] + result[y] + result[z])
    return realBookedRoom


def calRevenue(hotel:Hotel,shuttle:Shuttle)->int:
    """
    This function is to calculate the revenue of a certain hotel within a given time period.
    Hotel revenue comes from the number of accommodation rooms multiplied by the room price.
    To get the number of accommodation rooms, we should compare the real booked room number with the hotel room number.
    If the real booked room number is smaller than the hotel room number, which means that the hotel is not full, then we use the real booked room number to calculate the revenue of this hotel.
    If the real booked room number is greater than the hotel room number, which means that the hotel is full, then we use the hotel room number to calculate the revenue of this hotel.

    :param hotel: Hotel object, which represents a new hotel model in our simulation
    :param shuttle: Shuttle object, which represents a new shuttle model in our simulation
    :return: the revenue of a certain hotel within a given time period

    >>> calRevenue(1,1)
    Traceback (most recent call last):
    TypeError: Parameters need to be hotel model and shuttle model.
    """
    # Determine whether the parameters are correct
    if not isinstance(hotel, Hotel) or not isinstance(shuttle, Shuttle):
        raise TypeError('Parameters need to be hotel model and shuttle model.')

    roomNum=hotel.getRoomNum()
    totalPrice=hotel.getPrice()
    realBookedRoom=getBookedRoom(hotel,shuttle)
    # Compare the real booked room number with the room number of this hotel
    # if the hotel is not full
    if realBookedRoom < roomNum:
        revenue = realBookedRoom * totalPrice
    else:
    # if the hotel is full
        revenue = roomNum * totalPrice
    return revenue


def calCost(hotel:Hotel,shuttle:Shuttle)->int:
    """
    We define the hotel cost as shuttle service cost plus constructing cost per room.
    Room Constructing Cost:
    Firstly, we estimated the highest single room cost in Manhattan area based on this hotel report in 2017
    http://www.cushmanwakefield.us/en/research-and-insight/2017/focus-on-hotel-construction-costs-2017. You can
    see details in reference_roomcost file in Github.

    Then we analyzed the average apartment price in different location in New York(Brooklyn, Manhattan, Queen, Bronx, Staten Island)
    based on the reference https://www1.nyc.gov/site/finance/taxes/property-rolling-sales-data.page.
    And we concluded that like apartment, hotel room cost will be influenced by distance as well. Based on the plot,
    we define an inverse correlation between hotel room cost and distance.

    Finally we can get total room cost given hotel total room number.

    Shuttle Service Cost:
    The shuttle service cost is a given attribute of Shuttle class.

    :param hotel: Hotel object, which represents a new hotel model in our simulation
    :param shuttle: Shuttle object, which represents a new shuttle model in our simulation
    :return: Total cost of constructing and operating a hotel, which mainly includes the shuttle cost and hotel room's cost

    >>> calCost(1,1)
    Traceback (most recent call last):
    TypeError: Parameters need to be hotel model and shuttle model.
    """

    # Determine whether the parameters are correct
    if not isinstance(hotel, Hotel) or not isinstance(shuttle, Shuttle):
        raise TypeError('Parameters need to be hotel model and shuttle model.')
    # Calculate single room constructing cost
    distance = hotel.getDistance()
    roomNum = hotel.getRoomNum()
    DowntownCost = 950000  # Manhattan(highest) hotel cost
    singleRoomCost = DowntownCost / distance  # inverse correlation between hotel room cost and distance
    roomCost = singleRoomCost * roomNum
    cost=roomCost+shuttle.getCost()
    return cost


def simulation():
    """
    This function is to run multiple simulations and obtain the profit distributions.
    Plot frequency distributions and normal distribution curves for this hotel.

    Change the number of simulations to 100, 500, 1000, 5000 separately and analyze how will the profit distribution change.

    :return: the histograms and normal distribution curves for this hotel.
    """

    # List of profit results
    profitresult = []
    # the number of simulations
    for i in range(100):
        hotel = Hotel()
        shuttle = Shuttle()
        profit=calRevenue(hotel,shuttle)-calCost(hotel,shuttle)
        profitresult.append(profit[0])
    profitresult = np.array(profitresult)
    # calculate the mean and the standard deviation of the profit results
    mean = profitresult.mean()
    std=profitresult.std()
    # data visualization
    # plot the normal distribution curves
    x = np.arange(profitresult.min(),profitresult.max(),0.1)
    y = np.exp(-((x - mean) ** 2) / (2 * std ** 2)) / (std * np.sqrt(2 * np.pi))
    plt.plot(x, y)
    # plot the histograms
    plt.hist(profitresult, bins='auto',density=True)
    plt.title("Profit Average Level")
    plt.xlabel('Profit')
    plt.ylabel('Frequency')
    plt.show()


if __name__=='__main__':
    simulation()

# We will do four simulations, the simulation that we did in this file is simulation 4, you can see other simulation files under the folder Simulation in Github.
# simulation1: location changes
# simulation2: time changes
# simulation3: shuttle frequency changes
# simulation4: simulation number changes-----profit average level

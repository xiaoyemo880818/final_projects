
"""
In this simulation, we want to test how distance will influence the hotel overall profit level. So in this
simulation, our main variable is "distance". We suppose that the farther the hotel is away from city center,
the less profit it will get.
In order to test a general influence, we calculate the average profit of all our simulation hotel models,
which we think is a general tendency of all the hotels in New York city.

"""
import sympy
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import matplotlib.pyplot as pl
import copy

DAY=3000

class Hotel:
    """
    This class is about the hotel that we are going to construct. We define this class to generate random values of variables which are relevent to hotels
    It includes five attributes:
    :param roomNum: the number of rooms that this hotel will have
    :param guestType: the probability distribution of the guest types, which includes solo and business travellers (mostly one person per room), couple and friend travellers （mostly two persons per room) and family travellers (mostly three persons per room)
                      we refer to the dataset on https://www.kaggle.com/crawford/las-vegas-tripadvisor-reviews, you can see more details in Reference_guesttype in Github.
    :param priceSeed: the lowest price that used to generated the LowPriceInterval, MediumPriceInterval and HighPriceInterval
                      we refer to the dataset on https://www.kaggle.com/gdberrio/new-york-hotels, you can see more details in Reference_price_new_york_hotels.csv (column: "low rate") in Github.
    :param price: the sum of the price in the time period
    """

    __roomNum=np.random.random_integers(50, 2000, 1) # refer to Ctrip website
    __guestType=(0.19, 0.59, 0.22)  # 19% solo & business travelers, 59% couple & friend travelers, 22% family travelers
    __priceSeed=np.random.randint(50, 1000, 1) # a randomly generated number from interval [50,1000]
    __price=0 # the initialized price value of hotel

    def getRoomNum(self):
        return self.__roomNum
    def getDistance(self):
        return self.__distance
    def getGuestType(self):
        return self.__guestType
    def getPriceSeed(self):
        return self.__priceSeed
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


class Shuttle:
    """
    We define shuttle class to generate random value of variables relevant to shuttle service.
    :param dayCost- how much shuttle service will cost per day.
                    To define its value, we refer to this website http://www.freightmetrics.com.au/Calculators%7CRoad/BusOperatingCost/tabid/671/Default.aspx
                    We modify some parameters, like the type of bus and average passengers, to get the suitable cost.
                    You can see more details in Reference_shuttlecost file in Github.
    :param cost- The total cost of shuttle service for certain days
    :param shuttleFrequency-how many days the hotel will provide shuttle service within given days
                            Since shuttle service is a random variable and have only two choices, it satisfy
                            with binomial distribution.
    """
    __dayCost=790 # every day bus cost, reference----http://www.freightmetrics.com.au/Calculators%7CRoad/BusOperatingCost/tabid/671/Default.aspx
    __cost=0
    __shuttleFrequency=np.random.binomial(DAY,0.5,1) # shuttle is binomial

    def getCost(self):
        self.__cost=self.__dayCost*self.__shuttleFrequency
        return self.__cost

    def getFrequency(self):
        return self.__shuttleFrequency


def getGuestNum(shuttle:Shuttle,distance:int)->int:
    """
    Real Guest of hotel= Guests of hotel without shuttle + Guests brought by shuttle

    :param shuttle: Shuttle object, which represents a new shuttle model in our simulation
    :param distance: The distance between this hotel and the center of New York City (up to 30 miles), which is the main variable in our distance simulation
    :return: Calculated guest number of a certain hotel, which will be used to calculate the hotel revenue

    >>> getGuestNum(1,2)
    Traceback (most recent call last):
    TypeError: Parameters need to be hotel model and shuttle model.

    """
    # Determine whether the parameters are correct
    if not isinstance(shuttle, Shuttle):
        raise TypeError('Parameters need to be hotel model and shuttle model.')
    frequency=shuttle.getFrequency()
    # the number of air passenger per month
    GuestInterval=(7000000,11000000) # [7478511,11444185]  it is a uniform distribution
    TotalGuestNum=np.random.random_integers(GuestInterval[0],GuestInterval[1],1)*DAY/30
    HighestGuestRate=0.00018 # we calculate the rate by "number of reviews*rate of people post reviews/number of guest"
    LowestGuestRate=HighestGuestRate/2.5 # reference from TripAdvisor number of reviews
    k=(HighestGuestRate-LowestGuestRate)/30.0
    locationInfluence=HighestGuestRate-k*distance
    # since shuttle will bring more guests for hotels, we need to calculate its influence per day
    # 20 seat shuttle, go 5 round per day
    plusGuest = 100 * frequency  # this can be improved by random generating shuttle seats
    #plusGuest = shuttlePlusGuest * frequency
    # plusGuest = shuttlePlusGuest * frequency
    # Real Guest Number = Guests of hotel without shuttle + Guests brought by shuttle
    hotelGuestNum=TotalGuestNum*locationInfluence+plusGuest
    return hotelGuestNum


def getBookedRoom(hotel:Hotel,shuttle:Shuttle,distance:int)->int:
    """
    This function is to get the real booked room number according to the number of air passenger and the probability distribution of the guests.
    The guests are usually divided into three categories by the number of tourists travelling together, including single traveler, couple traveler and family traveler.
    With the guestType (obtained from https://www.kaggle.com/crawford/las-vegas-tripadvisor-reviews) and the GuestNum （calculated by the function getGuestNum), the real booked room number could be calculated by solving the equations.

    :param hotel: Hotel object, which represents a new hotel model in our simulation
    :param shuttle: Shuttle object, which represents a new shuttle model in our simulation
    :param distance: The distance between this hotel and the center of New York City (up to 30 miles), which is the main variable in our distance simulation
    :return: the real booked number of a certain hotel

    >>> getBookedRoom(1,1,2)
    Traceback (most recent call last):
    TypeError: Parameters need to be hotel model and shuttle model.
    """

    # Determine whether the parameters are correct
    if not isinstance(hotel, Hotel) or not isinstance(shuttle, Shuttle) or not int:
        raise TypeError('Parameters need to be hotel model and shuttle model and an integer.')
    # Solve ternary linear equations
    # x represents the booked number of single room, y represents the booked number of double room or twin room, z represents the booked number of triple room
    # Symbolize variables
    x = sympy.Symbol('x')
    y = sympy.Symbol('y')
    z = sympy.Symbol('z')
    guestType=hotel.getGuestType()
    hotelGuestNum = getGuestNum(hotel,shuttle,distance)
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


def calRevenue(hotel:Hotel,shuttle:Shuttle,distance:int)->int:
    """
    This function is to calculate the revenue of a certain hotel within a given time period.
    Hotel revenue comes from the number of accommodation rooms multiplied by the room price.
    To get the number of accommodation rooms, we should compare the real booked room number with the hotel room number.
    If the real booked room number is smaller than the hotel room number, which means that the hotel is not full, then we use the real booked room number to calculate the revenue of this hotel.
    If the real booked room number is greater than the hotel room number, which means that the hotel is full, then we use the hotel room number to calculate the revenue of this hotel.

    :param hotel: Hotel object, which represents a new hotel model in our simulation
    :param shuttle: Shuttle object, which represents a new shuttle model in our simulation
    :param distance: The distance between this hotel and the center of New York City (up to 30 miles), which is the main variable in our distance simulation
    :return: the revenue of a certain hotel within a given time period

    >>> calRevenue(1,1,2)
    Traceback (most recent call last):
    TypeError: Parameters need to be hotel model and shuttle model.
    """

    # Determine whether the parameters are correct
    if not isinstance(hotel, Hotel) or not isinstance(shuttle, Shuttle) or not int:
        raise TypeError('Parameters need to be hotel model and shuttle model and an integer.')
    roomNum=hotel.getRoomNum()
    totalPrice=hotel.getPrice()
    realBookedRoom=getBookedRoom(hotel,shuttle,distance)
    # Compare the real booked room number with the room number of this hotel
    # if the hotel is not full
    if realBookedRoom < roomNum:
        revenue = realBookedRoom * totalPrice
    # if the hotel is full
    else:
        revenue=roomNum * totalPrice
    return revenue


def calCost(hotel:Hotel,shuttle:Shuttle,distance:int)->int:
    """
    We define the hotel cost as shuttle service cost plus constructing cost per room.

    :param hotel: Hotel object, which represents a new hotel model in our simulation
    :param shuttle: Shuttle object, which represents a new shuttle model in our simulation
    :param distance: The distance between this hotel and the center of New York City (up to 30 miles), which is the main variable in our distance simulation
    :return: Total cost of constructing and operating a hotel, which mainly includes the shuttle cost and
             hotel room's cost

    >>> calCost(1,1,2)
    Traceback (most recent call last):
    TypeError: Parameters need to be hotel model and shuttle model.
    """
    # Determine whether the parameters are correct
    if not isinstance(hotel, Hotel) or not isinstance(shuttle, Shuttle):
        raise TypeError('Parameters need to be hotel model and shuttle model.')

    roomNum=hotel.getRoomNum()
    DowntownCost = 950000  # Manhattan(highest) hotel cost
    singleRoomCost = DowntownCost / distance  # reference from new york house price
    roomCost=singleRoomCost*roomNum
    cost=roomCost+shuttle.getCost()
    return cost


def distanceSimulation():
    """
    Change the value of distance and analyze its influence on hotel profit.In order to test a general
    influence, we calculate the average profit of all our simulation hotel models.

    :return:
    """
    # List of average simulation profit price for a certain distance value
    profitAVeList = []
    # change the value of distance
    for dis in np.arange(0.1,31.,0.5):
        # List of profit for every simulation
        profitList = []
        # simulation iteration
        for i in range(1000):
            hotel = Hotel()
            shuttle = Shuttle()
            profit=calRevenue(hotel,shuttle,dis)-calCost(hotel,shuttle,dis)
            profitList.append(profit)
        # Calculate the average profit
        profitAve = np.mean(profitList)
        profitAVeList.append(copy.deepcopy(profitAve))
    # Data visualization
    pl.xlabel("distance")
    pl.ylabel('profit')
    pl.xlim(0,30)
    pl.plot(np.arange(0.1,31.,0.5),profitAVeList, color='lightblue', linewidth=3)
    pl.savefig('./distance simulation.png')
    pl.show()


if __name__=='__main__':
    distanceSimulation()


# simulation1: location changes

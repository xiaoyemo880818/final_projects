
"""
In this simulation, we want to test how distance will influence the hotel overall profit level. So in this
simulation, our main variable is "distance". We suppose that the father the hotel is away from city center,
the less profit it will get.
In order to test a general influence, we calculate the average profit of all our simulation hotel model,
which we think is a general tendency of all the hotels in New York city.

"""
import sympy
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import matplotlib.pyplot as pl
import copy

DAY=3000


#LLY
class Hotel:

    __roomNum=np.random.random_integers(50, 2000, 1) # reference Ctrip website
    __guestType=(0.19, 0.59, 0.22)  # 19% solo & business,59% couples & friends,22% families
    __priceSeed=np.random.randint(50, 1000, 1) # a number random generate from interval [50,1000]
    __price=0

    def getRoomNum(self):
        return self.__roomNum
    def getDistance(self):
        return self.__distance
    def getGuestType(self):
        return self.__guestType
    def getPriceSeed(self):
        return self.__priceSeed
    def getPrice(self):
        # priceSeed = np.random.randint(50, 1000, 1)  # a number random generate from interval [50,1000]
        LowPriceInterval = (self.__priceSeed, self.__priceSeed * 1.5)  # X reference https://www.kaggle.com/gdberrio/new-york-hotels#
        MediumPriceInterval = (self.__priceSeed * 1.5, self.__priceSeed * 2)
        HighPriceInterval = (self.__priceSeed * 2, self.__priceSeed * 2.5)
        DayRandom = (0.25, 0.5, 0.25)  # X reference https://www.kaggle.com/airbnb/seattle#listings.csv
        lowPrice = np.random.random_integers(LowPriceInterval[0], LowPriceInterval[1], 1)  # From LowPrice
        mediumPrice = np.random.random_integers(MediumPriceInterval[0], MediumPriceInterval[1], 1)  # From MediumPrice
        highPrice = np.random.random_integers(HighPriceInterval[0], HighPriceInterval[1], 1)  # From HighPrice
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
    __dayCost=790
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

    :param hotel: Hotel object, which represents a new hotel model in our simulation
    :param shuttle: Shuttle object, which represents a new shuttle model in our simulation
    :param day: The timespan we defined to calculate the overall profit, which is
                the main variable in our time simulation experiment
    :return: Calculated guest number of a certain hotel, which will be used to calculate the hotel revenue

    >>> getGuestNum(1,1,2)
    Traceback (most recent call last):
    TypeError: Parameters need to be hotel model and shuttle model.

    """
    # Determine whether the parameters are correct
    if not isinstance(shuttle, Shuttle):
        raise TypeError('Parameters need to be hotel model and shuttle model.')
    frequency=shuttle.getFrequency()
    # the number of air passenger per month
    GuestInterval=(7000000,11000000)#[7478511,11444185]  it is a uniform distribution
    TotalGuestNum=np.random.random_integers(GuestInterval[0],GuestInterval[1],1)*DAY/30
    HighestGuestRate=0.00018   # !!!!!lack of reference!
    LowestGuestRate=HighestGuestRate/2.5  #reference from TripAdvisor number of reviews
    k=(HighestGuestRate-LowestGuestRate)/30.0
    locationInfluence=HighestGuestRate-k*distance
    # shuttle will bring more guest for hotel

    plusGuest = 100 * frequency  #!!!!!! 20 seat shuttle, go 5 round
    #plusGuest = shuttlePlusGuest * frequency

    hotelGuestNum=TotalGuestNum*locationInfluence+plusGuest
    return hotelGuestNum


# LLY
def getBookedRoom(hotel:Hotel,shuttle:Shuttle,distance:int)->int:
    x = sympy.Symbol('x')
    y = sympy.Symbol('y')
    z = sympy.Symbol('z')
    guestType=hotel.getGuestType()
    hotelGuestNum = getGuestNum(hotel,shuttle,distance)

    f1 = x + 2 * y + 3 * z - hotelGuestNum
    f2 = guestType[1] * x - guestType[0] * y
    f3 = guestType[2] * x - guestType[0] * z
    result = sympy.solve([f1, f2, f3], [x, y, z])
    realBookedRoom = int(result[x] + result[y] + result[z])
    return realBookedRoom

#LLY
def calRevenue(hotel:Hotel,shuttle:Shuttle,distance:int)->int:

    roomNum=hotel.getRoomNum()
    totalPrice=hotel.getPrice()
    realBookedRoom=getBookedRoom(hotel,shuttle,distance)

    if realBookedRoom < roomNum:
        revenue = realBookedRoom * totalPrice
    else:
        revenue=roomNum * totalPrice
    return revenue



def calCost(hotel:Hotel,shuttle:Shuttle,distance:int)->int:
    """
    We define the hotel cost as shuttle service cost plus constructing cost per room.

    :param hotel: Hotel object, which represents a new hotel model in our simulation
    :param shuttle: Shuttle object, which represents a new shuttle model in our simulation
    :param day: The timespan we defined to calculate the overall profit, which is
                the main variable in our time simulation experiment
    :return: Total cost of constructing and operating a hotel, which mainly includes the shuttle cost and
             hotel room's cost

    >>> getGuestNum(1,1,2)
    Traceback (most recent call last):
    TypeError: Parameters need to be hotel model and shuttle model.
    """
    # Determine whether the parameters are correct
    if not isinstance(hotel, Hotel) or not isinstance(shuttle, Shuttle):
        raise TypeError('Parameters need to be hotel model and shuttle model.')

    roomNum=hotel.getRoomNum()
    DowntownCost = 950000  # Manhattan hotel cost
    #distance = np.random.uniform(0, 30, 1)  # (0,30] miles---- reference from googlemap---
    singleRoomCost = DowntownCost / distance  # reference from new york house price
    roomCost=singleRoomCost*roomNum

    cost=roomCost+shuttle.getCost()
    return cost


def distanceSimulation():
    """
    Change the value of distance and analyze its influence on hotel profit.In order to test a general
    influence, we calculate the average profit of all our simulation hotel model.

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




# simulation3: roomNum & price change

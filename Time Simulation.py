
"""
In this simulation, we want to test how time will influence the hotel overall profit level. So in this
simulation, our main variable is time, which is "day" in our model.
In order to test a general influence, we calculate the average profit of all our simulation hotel model,
which we think is a general tendency of all the hotels in New York city.

"""
import sympy
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import matplotlib.pyplot as pl
import copy


#LLY
class Hotel:
    """


    """
    __distance=np.random.uniform(0, 30, 1) # (0,30] miles---- reference from googlemap---
    __roomNum=np.random.random_integers(50, 2000, 1)  # reference Ctrip website
    __guestType=(0.19, 0.59, 0.22)  # 19% solo & business,59% couples & friends,22% families
    __priceSeed=np.random.randint(50, 1000, 1)  # a number random generate from interval [50,1000]
    __price=0

    def getRoomNum(self):
        """

        :return:
        """
        return self.__roomNum
    def getDistance(self):
        """

        :return:
        """
        return self.__distance
    def getGuestType(self):
        """

        :return:
        """
        return self.__guestType
    def getPrice(self):
        """

        :return:
        """
        # priceSeed = np.random.randint(50, 1000, 1)  # a number random generate from interval [50,1000]
        LowPriceInterval = (self.__priceSeed, self.__priceSeed * 1.5)  # X reference https://www.kaggle.com/gdberrio/new-york-hotels#
        MediumPriceInterval = (self.__priceSeed * 1.5, self.__priceSeed * 2)
        HighPriceInterval = (self.__priceSeed * 2, self.__priceSeed * 2.5)
        DayRandom = (0.25, 0.5, 0.25)  # X reference https://www.kaggle.com/airbnb/seattle#listings.csv
        lowPrice = np.random.random_integers(LowPriceInterval[0], LowPriceInterval[1], 1)  # From LowPrice
        mediumPrice = np.random.random_integers(MediumPriceInterval[0], MediumPriceInterval[1], 1)  # From MediumPrice
        highPrice = np.random.random_integers(HighPriceInterval[0], HighPriceInterval[1], 1)  # From HighPrice
        self.__price = lowPrice * DayRandom[0] + mediumPrice * DayRandom[1] + highPrice * DayRandom[2]
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
    __shuttleFrequency=0

    def getFrequency(self,day):
        __shuttleFrequency = np.random.binomial(day, 0.5, 1)  # shuttle is binomial
        return self.__shuttleFrequency

    def getCost(self,day):
        self.__cost=self.__dayCost*self.getFrequency(day)
        return self.__cost


# Guest number of a certain hotel, suppose the guest number have linear negative relationship with distance

def getGuestNum(hotel:Hotel,shuttle:Shuttle,day:int)->int:
    """
    Overall air passengers:
    We know the overall air passengers arrived at New York's five airports based on Kaggle dataset-
    -https://www.kaggle.com/new-york-state/nys-air-passenger-traffic,-port-authority-of-ny-nj. You can see more
    details in reference_airpassenger file in Github.
    Guests of hotel without shuttle:
    In our simulation model, we suppose that distance will influence the guest number of a certain hotel.
    The farther away the hotel is from New York city center, the less guest it can get. Therefore, we define
    a negative linear relationship between variable GuestRate and variable distance, which means when the hotel
    is n miles closer to the city center, k*n percent of overall tourists they can get.(k is the slope)
    We get the highest guest rate and lowest guest rate from the number of reviews in TripAdvisor. You can see
    more details in reference_guestrate file in Github.
    Guests brought by shuttle:
    Since shuttle service will bring more guests for the hotel, we need to consider its influence.
    We suppose 20-seats-shuttle will go 5 round a day, so the guest number per day is 100.

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
    if not isinstance(hotel,Hotel) or not isinstance(shuttle,Shuttle):
        raise TypeError('Parameters need to be hotel model and shuttle model.')

    distance=hotel.getDistance()
    frequency=shuttle.getFrequency(day)
    # the number of air passenger per month
    GuestInterval=(7000000,11000000)#[7478511,11444185]  it is a uniform distribution
    TotalGuestNum= np.random.random_integers(GuestInterval[0],GuestInterval[1],1)*day/30
    HighestGuestRate=0.00018 # we calculate the rate by "number of reviews*rate of people post reviews/number of guest"
    LowestGuestRate=HighestGuestRate/2.5  #reference from TripAdvisor number of reviews
    k=(HighestGuestRate-LowestGuestRate)/30.0 #the range of variable distance is from 0 to 30 miles
    locationInfluence=HighestGuestRate-k*distance # we suppose a negative linear relationship
    # since shuttle will bring more guests for hotels, we need to calculate its influence per day
    # 20 seat shuttle, go 5 round per day
    plusGuest = 100 * frequency  # this can be improved by random generating shuttle seats
    # Real Guest Number=Par of Guest for hotel+ Shuttle brought Guest
    hotelGuestNum=TotalGuestNum*locationInfluence+plusGuest
    return hotelGuestNum


# LLY
def getBookedRoom(hotel:Hotel,shuttle:Shuttle,day:int)->int:
    x = sympy.Symbol('x')
    y = sympy.Symbol('y')
    z = sympy.Symbol('z')
    guestType=hotel.getGuestType()
    hotelGuestNum = getGuestNum(hotel,shuttle,day)

    f1 = x + 2 * y + 3 * z - hotelGuestNum
    f2 = guestType[1] * x - guestType[0] * y
    f3 = guestType[2] * x - guestType[0] * z
    result = sympy.solve([f1, f2, f3], [x, y, z])
    realBookedRoom = int(result[x] + result[y] + result[z])
    return realBookedRoom

#LLY
def calRevenue(hotel:Hotel,shuttle:Shuttle,day:int)->int:
    roomNum=hotel.getRoomNum()
    totalPrice=hotel.getPrice()*day
    realBookedRoom=getBookedRoom(hotel,shuttle,day)

    if realBookedRoom < roomNum:
        revenue = realBookedRoom * totalPrice
    else:
        revenue=roomNum * totalPrice
    return revenue



def calCost(hotel:Hotel,shuttle:Shuttle,day:int)->int:
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
    Finally we can get total room cost given hotel total room number
    Shuttle Service Cost:
    The shuttle service cost is a given attribute of Shuttle class.

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
    if not isinstance(hotel,Hotel) or not isinstance(shuttle,Shuttle):
        raise TypeError('Parameters need to be hotel model and shuttle model.')
    # Calculate single room constructing cost
    distance=hotel.getDistance()
    roomNum=hotel.getRoomNum()
    DowntownCost = 950000  # Manhattan(highest) hotel cost
    singleRoomCost = DowntownCost / distance  # inverse correlation between hotel room cost and distance
    roomCost=singleRoomCost*roomNum
    # Calculate the total cost of a certain hotel
    cost=roomCost+shuttle.getCost(day)
    return cost




def timeSimulation():
    """
    Change the value of time and analyze its influence on hotel profit.In order to test a general
    influence, we calculate the average profit of all our simulation hotel model.
    Generally, we will calculate the profit by using total revenue minus total cost. Since making money is
    a very slow process, we analyze time influence in "year".

    :return:
    """
    # List of average simulation profit price for a certain time value(year)
    profitAVeList=[]
    # change the value of time
    for year in range(1,21,1):
        # List of profit for every simulation
        profitList = []
        # simulation iteration
        for i in range(1000):
            hotel = Hotel()
            shuttle = Shuttle()
            profit = calRevenue(hotel, shuttle, 360 * year) - calCost(hotel, shuttle, 360 * year)
            profitList.append(profit)
        # Calculate the average profit
        profitAve=np.mean(profitList)
        profitAVeList.append(copy.deepcopy(profitAve))
    # Data visualization
    pl.xlabel("year")
    pl.ylabel('profit')
    pl.plot(range(1,21,1),profitAVeList, color='lightblue', linewidth=3)
    pl.xticks(range(1,21,1))
    pl.show()



if __name__=='__main__':
    timeSimulation()



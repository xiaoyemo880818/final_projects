# use Numpy to do the simulation
# calculate weekly profit= revenue-cost
import sympy
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

DAY=3000
# can create a class for hotel, have distance attribute, roomNum attribute, guestType attribute, price attribute
class Hotel:
    __distance=np.random.random_integers(50, 2000, 1)# reference Ctrip website
    __roomNum=np.random.uniform(0, 30, 1) # (0,30] miles---- reference from googlemap---
    __guestType=(0.19, 0.59, 0.22)  # 19% solo & business,59% couples & friends,22% families
    __priceSeed=np.random.randint(50, 1000, 1)  # a number random generate from interval [50,1000]
    __price=0

    def getRoomNum(self):
        return self.__roomNum
    def getDistance(self):
        return self.__distance
    def getGuestType(self):
        return self.__guestType
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


# can create a class for shuttle, have cost attribute, have passengerNum attribute, have shuttleFrequency attribute
class Shuttle:
    __dayCost=790 # every day bus cost reference----http://www.freightmetrics.com.au/Calculators%7CRoad/BusOperatingCost/tabid/671/Default.aspx
    __cost=0
    __shuttleFrequency=np.random.binomial(DAY,0.5,1)  # shuttle is binomial

    def getCost(self):
        self.__cost=self.__dayCost*self.__shuttleFrequency
        return self.__cost

    def getFrequency(self):
        return self.__shuttleFrequency



# *location
# suppose the guest number have linear negative relationship with distance

# Guest number of a certain hotel, suppose the guest number have linear negative relationship with distance

def getGuestNum(hotel:Hotel,shuttle:Shuttle)->int:
    distance=hotel.getDistance()
    frequency=shuttle.getFrequency()
    # the number of air passenger per month
    GuestInterval=(7000000,11000000)#[7478511,11444185]  it is a uniform distribution-----https://www.kaggle.com/new-york-state/nys-air-passenger-traffic,-port-authority-of-ny-nj
    TotalGuestNum=np.random.random_integers(GuestInterval[0],GuestInterval[1],1)
    HighestGuestRate=0.00018   # !!!!!lack of reference!
    LowestGuestRate=HighestGuestRate/2.5  #reference from TripAdvisor number of reviews
    k=(HighestGuestRate-LowestGuestRate)/30.0
    locationInfluence=HighestGuestRate-k*distance
    # shuttle will bring more guest for hotel

    plusGuest = 100 * frequency  #!!!!!! 20 seat shuttle, go 5 round
    #plusGuest = shuttlePlusGuest * frequency

    hotelGuestNum=TotalGuestNum*locationInfluence+plusGuest
    return hotelGuestNum

# *---- room price level----
# def getPrice()-> int:
#
#     priceSeed=np.random.randint(50,1000,1) # a number random generate from interval [50,1000]
#     LowPriceInterval=(priceSeed, priceSeed * 1.5) # X reference https://www.kaggle.com/gdberrio/new-york-hotels#
#     MediumPriceInterval=(priceSeed * 1.5, priceSeed * 2)
#     HighPriceInterval=(priceSeed * 2, priceSeed * 2.5)
#     DayRandom=(0.25,0.5,0.25) # X reference https://www.kaggle.com/airbnb/seattle#listings.csv
#     lowPrice=np.random.random_integers(LowPriceInterval[0], LowPriceInterval[1], 1)# From LowPrice
#     mediumPrice=np.random.random_integers(MediumPriceInterval[0], MediumPriceInterval[1], 1)# From MediumPrice
#     highPrice=np.random.random_integers(HighPriceInterval[0], HighPriceInterval[1], 1)# From HighPrice
#     totalPrice=(lowPrice*DayRandom[0]+mediumPrice*DayRandom[1]+highPrice*DayRandom[2])*DAY
#     return totalPrice

def getBookedRoom(hotel:Hotel,shuttle:Shuttle)->int:
    x = sympy.Symbol('x')
    y = sympy.Symbol('y')
    z = sympy.Symbol('z')
    guestType=hotel.getGuestType()
    hotelGuestNum = getGuestNum(hotel,shuttle)

    f1 = x + 2 * y + 3 * z - hotelGuestNum
    f2 = guestType[1] * x - guestType[0] * y
    f3 = guestType[2] * x - guestType[0] * z
    result = sympy.solve([f1, f2, f3], [x, y, z])
    realBookedRoom = int(result[x] + result[y] + result[z])
    return realBookedRoom

def calRevenue(hotel:Hotel,shuttle:Shuttle)->int:
    # *---- room number---- random number[uniform distribution]
    # get the distribution of people's travel type-- https://www.kaggle.com/enikolov/reviews-tripadvisor-hotels-and-edmunds-cars/data
    # analyze GuestType by https://www.kaggle.com/crawford/las-vegas-tripadvisor-reviews
    # GuestType = (0.19, 0.59, 0.22)  # 19% solo & business,59% couples & friends,22% families
    # roomNum = np.random.random_integers(50, 2000, 1)  # reference Ctrip website
    #guestType=hotel.getGuestType()
    roomNum=hotel.getRoomNum()
    totalPrice=hotel.getPrice()
    realBookedRoom=getBookedRoom(hotel,shuttle)


    if realBookedRoom < roomNum:
        revenue = realBookedRoom * totalPrice
    else:
        revenue=roomNum * totalPrice
    return revenue



def calCost(hotel:Hotel,shuttle:Shuttle)->int:
    # room cost
    distance=hotel.getDistance()
    roomNum=hotel.getRoomNum()
    DowntownCost = 950000  # Manhattan hotel cost http://www.cushmanwakefield.us/en/research-and-insight/2017/focus-on-hotel-construction-costs-2017
    #distance = np.random.uniform(0, 30, 1)  # (0,30] miles---- reference from googlemap---
    singleRoomCost = DowntownCost / distance  # reference from new york house price----https://www1.nyc.gov/site/finance/taxes/property-rolling-sales-data.page
    roomCost=singleRoomCost*roomNum

    #shuttleFrequency = np.random.binomial()  # shuttle is binomial
  #  shuttleDayCost = 790  # every day bus cost reference----http://www.freightmetrics.com.au/Calculators%7CRoad/BusOperatingCost/tabid/671/Default.aspx
  #  shuttleCost=shuttleDayCost*shuttleFrequency

    cost=roomCost+shuttle.getCost()
    return cost


# for-loop to do simulation and output the result
def simulation():
    for i in range(100):
        #
        hotel = Hotel()
        shuttle = Shuttle()
        profit=calRevenue(hotel,shuttle)-calCost(hotel,shuttle)
        print(profit)

if __name__=='__main__':
    simulation()

# visualization the result
def visualProfit():
    pass

# simulation1: only time change
# simulation2: only distance change
# simulation3: roomNum & price change

# simulation4: whether have shuttle or not change
# simulation5: shuttle frequency change
# simulation6: simulation number change-----profit average level
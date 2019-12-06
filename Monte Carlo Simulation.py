# use Numpy to do the simulation
# calculate weekly profit= revenue-cost
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# calculate cost
# room cost
DowntownCost=950000 # Manhattan hotel cost http://www.cushmanwakefield.us/en/research-and-insight/2017/focus-on-hotel-construction-costs-2017
distance=np.random.uniform(0, 30, 1) #(0,30] miles---- reference from googlemap---
singleRoomCost=DowntownCost/distance # reference from new york house price----https://www1.nyc.gov/site/finance/taxes/property-rolling-sales-data.page

#  * ---- shuttle cost--- from real-world data  cost---- https://www.kaggle.com/dansbecker/new-york-city-taxi-fare-prediction
# shuttle is binomial
shuttleCost=790  #every day bus cost reference----http://www.freightmetrics.com.au/Calculators%7CRoad/BusOperatingCost/tabid/671/Default.aspx
plusGuest=100*GuestType

# *location
# suppose the guest number have linear negative relationship with distance

# Guest number of a certain hotel,nsuppose the guest number have linear negative relationship with distance
def getGuestNum()->int:
    GuestInterval=(7000000,11000000)#[7478511,11444185]  it is a uniform distribution-----https://www.kaggle.com/new-york-state/nys-air-passenger-traffic,-port-authority-of-ny-nj
    TotalGuestNum=np.random.random_integers(GuestInterval[0],GuestInterval[1],1)
    HighestGuestRate=0.00018   # !!!!!lack of reference!
    LowestGuestRate=HighestGuestRate/2.5  #reference from TripAdvisor number of reviews
    k=(HighestGuestRate-LowestGuestRate)/30.0
    locationInfluence=HighestGuestRate-k*distance
    hotelGuestNum=TotalGuestNum*locationInfluence
    return hotelGuestNum


# calculate revenue

# *---- room price level----
def getPrice()-> int:
    TotalDay=30
    priceSeed=np.random.randint(50,1000,1) # a number random generate from interval [50,1000]
    LowPriceInterval=(priceSeed, priceSeed * 1.5) # X reference https://www.kaggle.com/gdberrio/new-york-hotels#
    MediumPriceInterval=(priceSeed * 1.5, priceSeed * 2)
    HighPriceInterval=(priceSeed * 2, priceSeed * 2.5)

    DayRandom=(0.25,0.5,0.25) # X reference https://www.kaggle.com/airbnb/seattle#listings.csv
    lowPrice=np.random.random_integers(LowPriceInterval[0], LowPriceInterval[1], 1)# From LowPrice
    mediumPrice=np.random.random_integers(MediumPriceInterval[0], MediumPriceInterval[1], 1)# From MediumPrice
    highPrice=np.random.random_integers(HighPriceInterval[0], HighPriceInterval[1], 1)# From HighPrice

    totalPrice=(lowPrice*DayRandom[0]+mediumPrice*DayRandom[1]+highPrice*DayRandom[2])*TotalDay
    return totalPrice




def calRevenue(totalPrice:int,hotelGuestNum:int)->int:
    # *---- room number---- random number[uniform distribution]
    # get the distribution of people's travel type-- https://www.kaggle.com/enikolov/reviews-tripadvisor-hotels-and-edmunds-cars/data
    # analyze GuestType by https://www.kaggle.com/crawford/las-vegas-tripadvisor-reviews
    roomNum = np.random.random_integers(50, 2000, 1)  # reference Ctrip website
    GuestType = (0.19, 0.59, 0.22)  # 19% solo & business,59% couples & friends,22% families
    realBookedRoom = int(GuestType[0] * hotelGuestNum + GuestType[1] * hotelGuestNum / 2 + GuestType[2] * hotelGuestNum / 3)
    if realBookedRoom < roomNum:
        revenue = realBookedRoom * totalPrice
    else:
        revenue=roomNum*totalPrice
    return revenue


def calCost():
    pass


# for-loop to do simulation and output the result


# visualization the result
def visualProfit():
    pass
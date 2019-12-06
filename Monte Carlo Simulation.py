# use Numpy to do the simulation
# calculate weekly profit= revenue-cost
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

TotalGuestNum= 10000000
# # total number of guest-----https://www.kaggle.com/new-york-state/nys-air-passenger-traffic,-port-authority-of-ny-nj
#
#
#
# # calculate cost
# # Manhattan hotel cost http://www.cushmanwakefield.us/en/research-and-insight/2017/focus-on-hotel-construction-costs-2017
# DowntownCost=950000
# distance=np.random.   #(0,30] miles---- reference from googlemap---
# singleRoomCost=DowntownCost/distance # reference from newyork house price----https://www1.nyc.gov/site/finance/taxes/property-rolling-sales-data.page
#
#
# # * ---- shuttle cost--- from real-world data  cost---- https://www.kaggle.com/dansbecker/new-york-city-taxi-fare-prediction
# # shuttle is binomial
# shuttleCost=790  #every day bus cost reference----http://www.freightmetrics.com.au/Calculators%7CRoad/BusOperatingCost/tabid/671/Default.aspx
# plusGuest=100*GuestType



# *location
# suppose the guest number have linear negative relationship with distance
distance=np.random.uniform(0, 30, 1)
HighestGuestRate= 0.00018   # !!!!!lack of reference!
LowestGuestRate=HighestGuestRate/2.5  #reference from TripAdvisor number of reviews
k=(HighestGuestRate-LowestGuestRate)/30.0
locationInfluence=HighestGuestRate-k*distance


# calculate revenue

# *---- room number---- random number[uniform distribution]
# get the distribution of people's travel type-- https://www.kaggle.com/enikolov/reviews-tripadvisor-hotels-and-edmunds-cars/data
# analyze GuestType by https://www.kaggle.com/crawford/las-vegas-tripadvisor-reviews
roomNum=np.random.random_integers(50, 2000, 1)  # reference Ctrip website
GuestType=(0.19, 0.59, 0.22) #19% solo & business,59% couples & friends,22% families
HotelGuestNum=TotalGuestNum*locationInfluence
realBookedRoom=int(GuestType[0]*HotelGuestNum+GuestType[1]*HotelGuestNum/2+GuestType[2]*HotelGuestNum/3)
if realBookedRoom < roomNum:
    revenue=realBookedRoom*price
# else revenue=roomNum*price




# # *---- room price level---- from real-world data find distribution
# #                         https://www.kaggle.com/airbnb/seattle
# TotalDay=7
# #priceSeed= a number random generate from interval [50,1000]
# LowPrice=[priceSeed,priceSeed*1.5] #reference https://www.kaggle.com/gdberrio/new-york-hotels#
# MediumPrice=[priceSeed*1.5,priceSeed*2]
# HighPrice=[priceSeed*2,priceSeed*2.5]
#
# dayRandom=(0.25,0.5,0.25) #total day is 7 and random generate a array
# lowPriceRandom=np.random.# From LowPrice
# mediumPriceRandom=np.random.# From MediumPrice
# highPriceRandom=np.random.# From HighPrice
#
#
# # for-loop to do simulation and output the result
#
#
#
#
#
# # visualization the result

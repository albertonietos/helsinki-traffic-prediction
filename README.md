# HTML: Helsinki Traffic monitoring with Machine Learning

The final product of our project has been deployed at [helsinki-traffic-monitoring.herokuapp.com](https://helsinki-traffic-monitoring.herokuapp.com/).
Feel free to use it and give feedback on possible future improvements.

## A. TITLE: **HTML** (**H**elsinki **T**raffic monitoring with **M**achine **L**earning)

## B. ELEVATOR PITCH

The target group is people mainly using cars near a TMS (Traffic Measurement System)station (e.g. near Kumpula Campus). It addresses the need for predicting what the traffic will be like in a given hour and if there is a decrease in speed due to traffic. By using real world data we can predict relatively accurately what the traffic will be at a given time.

## C. DATA

We will be using the [**Digitraffic API**](https://www.digitraffic.fi/en/road-traffic/) to get real world data of the traffic near a specific location. We will include traffic going both ways near this location in our analysis.
The data will be gathered through the API to create a training set used for machine learning.

Depending on the noise in the data there will be some cleaning involved. At least one feature not in the data is the day of the week the data is collected on. The hypothesis is that weekends have different amounts of traffic than weekdays so this needs to be considered by our model. Other seasonal effects such as public holidays (e.g. Christmas or Midsummer) will also be taken into consideration when engineering the features to input the model.

In order to enhance the information available to the user, we will also use data from the [**Helsinki Region Travel Time Matrix 2018**](https://blogs.helsinki.fi/accessibility/helsinki-region-travel-time-matrix-2018/) compiled by the Accessibility and mobility research within Digital Geography Lab at Univerity of Helsinki.
While our predictions will be based on real-time data, this other data will help us offer alternative means of transportation to the user.

## D. DATA ANALYSIS

We try to learn what the traffic patterns are on a given station. Our analysis will focus on the amount of vehicles that pass by a sensor. The data also includes information on the speeds of the vehicles so we might include this also into the analysis.
Our machine learning model will most likely be a linear regression model that predicts traffic congestion based on a timestamp.
Feature engineering will be utilized to be able to capture trends and seasonality.

## E. COMMUNICATION OF RESULTS

We are planning to offer a prediction of the road traffic at a given time and offer some recommendations based on that information. For example, if the traffic state is above normal levels we can offer information on other transportation means such as biking or public transport.
In order to improve our service we will be showing some geospatial visualizations to compare alternative ways of transportation.
Following the principle "Show, don't tell" will give th user a better experience and will reduce the time needed to get all the information they need.

## F. OPERATIONALIZATION

This service can help the user make informed decisions about whether it is a good idea to choose the car as a transportation need and whether the traffic state at that time is optimal. If the time is not optimal (i.e. rush hour), it can suggest other times when congestion is less likely.

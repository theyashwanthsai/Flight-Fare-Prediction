import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from datetime import datetime
import datetime
import pickle
from predict import predict
import matplotlib.pyplot as plt



# Methods




st.cache_data()
def load_data():
    train_data = pd.read_excel('Flight Dataset/Data_Train.xlsx')

    def newd(x):
        if x=='New Delhi':
            return 'Delhi'
        else:
            return x

    # Extract day and month columns from Date_of_journey column
    train_data['Destination'] = train_data['Destination'].apply(newd)
    train_data['Journey_day'] = pd.to_datetime(train_data['Date_of_Journey'],format='%d/%m/%Y').dt.day
    train_data['Journey_month'] = pd.to_datetime(train_data['Date_of_Journey'],format='%d/%m/%Y').dt.month

    train_data.drop('Date_of_Journey',inplace=True,axis=1)
    train_data.drop(['Route', 'Additional_Info'], axis=1, inplace=True)

    # Extracting hours and minutes from departure and arrival time
    train_data['Dep_hour'] = pd.to_datetime(train_data['Dep_Time']).dt.hour
    train_data['Dep_min'] = pd.to_datetime(train_data['Dep_Time']).dt.minute
    train_data.drop('Dep_Time',axis=1,inplace=True) #drop the departure time column
    train_data['Arrival_hour'] = pd.to_datetime(train_data['Arrival_Time']).dt.hour
    train_data['Arrival_min'] = pd.to_datetime(train_data['Arrival_Time']).dt.minute
    train_data.drop('Arrival_Time',axis=1,inplace=True) #drop the arrival time column

    # Dropping the Duration column and extracting important info(Hour and Minute) from it
    duration = list(train_data['Duration'])
    for i in range(len(duration)):
        if len(duration[i].split()) != 2:
            if 'h' in duration[i]:
                duration[i] = duration[i] + ' 0m'
            else:
                duration[i] = '0h ' + duration[i]
    duration_hour = []
    duration_min = []
    for i in duration:
        h,m = i.split()
        duration_hour.append(int(h[:-1]))
        duration_min.append(int(m[:-1]))
    train_data['Duration_hours'] = duration_hour
    train_data['Duration_mins'] = duration_min
    train_data.drop('Duration',axis=1,inplace=True)

    #change total_stops
    train_data['Total_Stops'].replace({'non-stop':0,'1 stop':1,'2 stops':2,'3 stops':3,'4 stops':4},inplace=True)

    return train_data

st.cache_resource()
def load_model():
    model = pickle.load(open('model/flight_rf.pkl','rb'))
    return model




# GUI



st.image("image.webp")
st.title('Flights Fare Prediction')

st.sidebar.header("Recommendations based on historic data")
st.sidebar.subheader("Based on the dataset")
st.sidebar.success("Most Popular Airline:  :white[Jet Airways, Indigo]")
st.sidebar.success("Most Popular Destinations:  :white[Cochin, Bangalore, Delhi]")
st.sidebar.success("Direct flights with 0 stops are significantly cheaper")
st.sidebar.success("Best time to book the flight: Afternoon 1pm")
# st.sidebar.markdown('<span style="background-color: green; color: white;">**Most Popular Airline: Indigo**</span>', unsafe_allow_html=True)


st.write('### Flight Fare Prediction using Machine Learning model.')
with st.form("Flight_prediction_form"):
    st.write("Please fill the following:")
    col1, col2 = st.columns(2)
    with col1:
        sources = ['Delhi', 'Kolkata', 'Banglore', 'Mumbai', 'Chennai']
        src_choice = st.selectbox('Source', sources)
        today = datetime.date.today()
        # departure_date = st.date_input('Departure date', today)
        # departure_time = st.time_input('Departure time', datetime.time(8, 45))
        
        stops = [0,1,2,3,4]
        stop_choice = st.selectbox('No. of Stops', stops)
        

        

    with col2:
        destinations = ['Cochin',  'Banglore', 'Delhi','Hyderabad', 'Kolkata',]
        dest_choice = st.selectbox('Destination', destinations)
        today = datetime.date.today()
        

        today = datetime.date.today()
        # arrival_date = st.date_input('Arrival date', today)
        # arrival_time = st.time_input('Arrival time', datetime.time(8, 45))
        # arrival_date = departure_date
        # arrival_time = departure_time
        # airlines = ['Jet Airways', 'IndiGo', 'Air India',
        # 'Multiple carriers', 'SpiceJet', 'Vistara',
        # 'GoAir', 'Multiple carriers Premium economy',
        # 'Jet Airways Business', 'Vistara Premium economy',
        # 'Trujet']
        # airline_choice = st.selectbox('Which Airline?', airlines)
        nummm = [1,2,3,4]
        num_choice = st.selectbox('No. of tickets', nummm)
        # Every form must have a submit button.
    # nummm = [1,2,3,4]
    # num_choice = st.selectbox('No. of tickets', nummm)
    airlines = ['Jet Airways', 'IndiGo', 'Air India',
        'Multiple carriers', 'SpiceJet', 'Vistara',
        'GoAir', 'Multiple carriers Premium economy',
        'Jet Airways Business', 'Vistara Premium economy',
        'Trujet']
    airline_choice = st.selectbox('Which Airline?', airlines)
    departure_date = st.date_input('Select a date', today)
    # departure_time = st.time_input('Departure time', datetime.time(8, 45))
    departure_time = datetime.time(8,45)
    arrival_date = departure_date
    arrival_time = departure_time
    # start_date = departure_date - pd.DateOffset(days=5)
    # end_date = departure_date + pd.DateOffset(days=5)
    
    
    submitted = st.form_submit_button("Submit")
    if submitted:

        # if arrival_date<departure_date:
        #     st.error('Arrival date must be later than Departure date!!!')
        # elif arrival_date==departure_date and arrival_time < departure_time:
        #     st.error('Arrival time must be later than the departure time!!!')
        if src_choice == dest_choice:
            st.error('Source and Destination must be different!')
        else:
            col1, col2 = st.columns(2)

        with col1:
                st.write("- Source:", src_choice,)
                st.write("- Destination:", dest_choice)
                st.write("- No. of Stops:", stop_choice)
        with col2:
                st.write("- Airline:", airline_choice)
                dep_time = departure_date.strftime("%Y-%m-%d") + ' '+ departure_time.strftime("%H:%M")
                arr_time = arrival_date.strftime("%Y-%m-%d") + ' '+ arrival_time.strftime("%H:%M")
                # st.write("- Departure Time:", dep_time)
                # st.write("- Arrival time:", arr_time)
                st.write("- No of Tickets:", num_choice)
                st.write("- Date:", arrival_date)

        model = pickle.load(open('model/flight_rf.pkl','rb'))

# Predict prices for IndiGo
        # price = predict(model, dep_time=dep_time, arrival_time=arr_time, Total_stops=stop_choice, airline= airline_choice, source=src_choice, destination=dest_choice)

        # st.success("**Predicted flight price:** :green[**{}**]".format(price))
        pricelist = []
        # pricebefore = []
        datelist = []
        for i in range(5):
            datenew = departure_date - pd.DateOffset(days = i)
            datelist.append(datenew)
            dep_time = datenew.strftime("%Y-%m-%d") + ' '+ datenew.strftime("%H:%M")
            arr_time = datenew.strftime("%Y-%m-%d") + ' '+ datenew.strftime("%H:%M")
            price = predict(model, dep_time=dep_time, arrival_time=arr_time, Total_stops=stop_choice, airline= airline_choice, source=src_choice, destination=dest_choice)
            # st.success("**Predicted flight price:** :green[**{}**]".format(price))
            price = price*num_choice
            pricelist.append(price)
        pricelist.reverse()
        datelist.reverse()
        departure_date = departure_date + pd.DateOffset(days = 1)    
        for i in range(5):
            datenew = departure_date + pd.DateOffset(days = i)
            datelist.append(datenew)
            dep_time = datenew.strftime("%Y-%m-%d") + ' '+ datenew.strftime("%H:%M")
            arr_time = datenew.strftime("%Y-%m-%d") + ' '+ datenew.strftime("%H:%M")
            price = predict(model, dep_time=dep_time, arrival_time=arr_time, Total_stops=stop_choice, airline= airline_choice, source=src_choice, destination=dest_choice)
            # st.success("**Predicted flight price:** :green[**{}**]".format(price))
            price = price*num_choice
            pricelist.append(price)
        # print(datelist)
        # print(pricelist)
        # for i in range(10):
            # st.success("**Predicted flight price:** :green[**{}**]".format(pricelist[i]))
        plt.plot(datelist, pricelist)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Ticket Prices')
        plt.xticks(rotation=45)
        st.pyplot(plt)

# Find the index of the minimum price
        min_price_index = pricelist.index(min(pricelist))

# Find the index of the maximum price
        max_price_index = pricelist.index(max(pricelist))

# Retrieve the corresponding dates
        min_price_date = datelist[min_price_index].strftime('%Y-%m-%d')
        max_price_date = datelist[max_price_index].strftime('%Y-%m-%d')
        st.success("**Cheapest flight price on:** :green[**{}**] at Rs :green[**{}.**]".format(min_price_date, min(pricelist)))
        st.error("**Please dont book on:** :red[**{}.**] Estimated Price is at Rs :red[**{}.**]".format(max_price_date, max(pricelist)))
# ['Jet Airways', 'IndiGo', 'Air India',
#         'Multiple carriers', 'SpiceJet', 'Vistara',
#         'GoAir', 'Multiple carriers Premium economy',
#         'Jet Airways Business', 'Vistara Premium economy',
#         'Trujet']



# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from PIL import Image
# from datetime import datetime
# import datetime
# import pickle
# from predict import predict




# # Methods




# st.cache_data()
# def load_data():
#     train_data = pd.read_excel('Flight Dataset/Data_Train.xlsx')

#     def newd(x):
#         if x=='New Delhi':
#             return 'Delhi'
#         else:
#             return x

#     # Extract day and month columns from Date_of_journey column
#     train_data['Destination'] = train_data['Destination'].apply(newd)
#     train_data['Journey_day'] = pd.to_datetime(train_data['Date_of_Journey'],format='%d/%m/%Y').dt.day
#     train_data['Journey_month'] = pd.to_datetime(train_data['Date_of_Journey'],format='%d/%m/%Y').dt.month

#     train_data.drop('Date_of_Journey',inplace=True,axis=1)
#     train_data.drop(['Route', 'Additional_Info'], axis=1, inplace=True)

#     # Extracting hours and minutes from departure and arrival time
#     train_data['Dep_hour'] = pd.to_datetime(train_data['Dep_Time']).dt.hour
#     train_data['Dep_min'] = pd.to_datetime(train_data['Dep_Time']).dt.minute
#     train_data.drop('Dep_Time',axis=1,inplace=True) #drop the departure time column
#     train_data['Arrival_hour'] = pd.to_datetime(train_data['Arrival_Time']).dt.hour
#     train_data['Arrival_min'] = pd.to_datetime(train_data['Arrival_Time']).dt.minute
#     train_data.drop('Arrival_Time',axis=1,inplace=True) #drop the arrival time column

#     # Dropping the Duration column and extracting important info(Hour and Minute) from it
#     duration = list(train_data['Duration'])
#     for i in range(len(duration)):
#         if len(duration[i].split()) != 2:
#             if 'h' in duration[i]:
#                 duration[i] = duration[i] + ' 0m'
#             else:
#                 duration[i] = '0h ' + duration[i]
#     duration_hour = []
#     duration_min = []
#     for i in duration:
#         h,m = i.split()
#         duration_hour.append(int(h[:-1]))
#         duration_min.append(int(m[:-1]))
#     train_data['Duration_hours'] = duration_hour
#     train_data['Duration_mins'] = duration_min
#     train_data.drop('Duration',axis=1,inplace=True)

#     #change total_stops
#     train_data['Total_Stops'].replace({'non-stop':0,'1 stop':1,'2 stops':2,'3 stops':3,'4 stops':4},inplace=True)

#     return train_data

# st.cache_resource()
# def load_model():
#     model = pickle.load(open('model/flight_rf.pkl','rb'))
#     return model




# # GUI



# st.image("image.webp")
# st.title('Flights Fare Prediction')

# st.sidebar.header("Recommendations based on historic data")
# st.sidebar.subheader("Based on the dataset")
# st.sidebar.success("Most Popular Airline:  :white[Jet Airways, Indigo]")
# st.sidebar.success("Most Popular Destinations:  :white[Cochin, Bangalore, Delhi]")
# st.sidebar.success("Direct flights with 0 stops are significantly cheaper")
# st.sidebar.success("Best time to book the flight: Afternoon 1pm")
# # st.sidebar.markdown('<span style="background-color: green; color: white;">**Most Popular Airline: Indigo**</span>', unsafe_allow_html=True)


# st.write('### Flight Fare Prediction using Machine Learning model.')
# with st.form("Flight_prediction_form"):
#     st.write("Please fill the following:")
#     col1, col2 = st.columns(2)
#     with col1:
#         sources = ['Delhi', 'Kolkata', 'Banglore', 'Mumbai', 'Chennai']
#         src_choice = st.selectbox('Source', sources)
#         today = datetime.date.today()
#         departure_date = st.date_input('Departure date', today)
#         departure_time = st.time_input('Departure time', datetime.time(8, 45))
        

        

        

#     with col2:
#         destinations = ['Cochin',  'Banglore', 'Delhi','Hyderabad', 'Kolkata',]
#         dest_choice = st.selectbox('Destination', destinations)
#         today = datetime.date.today()
        

#         today = datetime.date.today()
#         arrival_date = st.date_input('Arrival date', today)
#         arrival_time = st.time_input('Arrival time', datetime.time(8, 45))
        
#         # airlines = ['Jet Airways', 'IndiGo', 'Air India',
#         # 'Multiple carriers', 'SpiceJet', 'Vistara',
#         # 'GoAir', 'Multiple carriers Premium economy',
#         # 'Jet Airways Business', 'Vistara Premium economy',
#         # 'Trujet']
#         # airline_choice = st.selectbox('Which Airline?', airlines)
        
#         # Every form must have a submit button.
#     stops = [0,1,2,3,4]
#     stop_choice = st.selectbox('No. of Stops', stops)
#     submitted = st.form_submit_button("Submit")
#     if submitted:

#         if arrival_date<departure_date:
#             st.error('Arrival date must be later than Departure date!!!')
#         elif arrival_date==departure_date and arrival_time < departure_time:
#             st.error('Arrival time must be later than the departure time!!!')
#         elif src_choice == dest_choice:
#             st.error('Source and Destination must be different!')
#         else:
#             col1, col2 = st.columns(2)

#         with col1:
#                 st.write("- Source:", src_choice,)
#                 st.write("- Destination:", dest_choice)
#                 st.write("- No. of Stops:", stop_choice)
#         with col2:
#                 # st.write("- Airline:", airline_choice)
#                 dep_time = departure_date.strftime("%Y-%m-%d") + ' '+ departure_time.strftime("%H:%M")
#                 arr_time = arrival_date.strftime("%Y-%m-%d") + ' '+ arrival_time.strftime("%H:%M")
#                 st.write("- Departure Time:", dep_time)
#                 st.write("- Arrival time:", arr_time)

#         model = pickle.load(open('model/flight_rf.pkl','rb'))
#        # Predict prices for Jet Airways
#         priceJet = predict(model, dep_time=dep_time, arrival_time=arr_time, Total_stops=stop_choice, airline='Jet Airways', source=src_choice, destination=dest_choice)

# # Predict prices for IndiGo
#         priceIndiGo = predict(model, dep_time=dep_time, arrival_time=arr_time, Total_stops=stop_choice, airline='IndiGo', source=src_choice, destination=dest_choice)

# # Predict prices for Air India
#         priceAirIndia = predict(model, dep_time=dep_time, arrival_time=arr_time, Total_stops=stop_choice, airline='Air India', source=src_choice, destination=dest_choice)

# # Predict prices for Multiple carriers
#         priceMultipleCarriers = predict(model, dep_time=dep_time, arrival_time=arr_time, Total_stops=stop_choice, airline='Multiple carriers', source=src_choice, destination=dest_choice)

# # Predict prices for SpiceJet
#         priceSpiceJet = predict(model, dep_time=dep_time, arrival_time=arr_time, Total_stops=stop_choice, airline='SpiceJet', source=src_choice, destination=dest_choice)

# # Predict prices for Vistara
#         priceVistara = predict(model, dep_time=dep_time, arrival_time=arr_time, Total_stops=stop_choice, airline='Vistara', source=src_choice, destination=dest_choice)

# # Predict prices for GoAir
#         priceGoAir = predict(model, dep_time=dep_time, arrival_time=arr_time, Total_stops=stop_choice, airline='GoAir', source=src_choice, destination=dest_choice)

# # Predict prices for Multiple carriers Premium economy
#         priceMultipleCarriersPremiumEconomy = predict(model, dep_time=dep_time, arrival_time=arr_time, Total_stops=stop_choice, airline='Multiple carriers Premium economy', source=src_choice, destination=dest_choice)

#         coll1, coll2 = st.columns(2)

#         with coll1:
            
#         # Display the predicted flight price for Jet Airways
#             st.success("**Predicted flight price for Jet Airways:** :green[**{}**]".format(priceJet))

#         # Display the predicted flight price for IndiGo
#             st.success("**Predicted flight price for IndiGo:** :green[**{}**]".format(priceIndiGo))

#         # Display the predicted flight price for Air India
#             st.success("**Predicted flight price for Air India:** :green[**{}**]".format(priceAirIndia))

#         # Display the predicted flight price for Multiple carriers
#             st.success("**Price for Multiple carriers:** :green[**{}**]".format(priceMultipleCarriers))

#         with coll2:
#         # Display the predicted flight price for Multiple carriers Premium economy
#             st.success("**Predicted flight price for Multiple carriers Premium economy:** :green[**{}**]".format(priceMultipleCarriersPremiumEconomy))
            
#         # Display the predicted flight price for SpiceJet
#             st.success("**Predicted flight price for SpiceJet:** :green[**{}**]".format(priceSpiceJet))

#         # Display the predicted flight price for Vistara
#             st.success("**Predicted flight price for Vistara:** :green[**{}**]".format(priceVistara))

#         # Display the predicted flight price for GoAir
#             st.success("**Predicted flight price for GoAir:** :green[**{}**]".format(priceGoAir))

        



# ['Jet Airways', 'IndiGo', 'Air India',
#         'Multiple carriers', 'SpiceJet', 'Vistara',
#         'GoAir', 'Multiple carriers Premium economy',
#         'Jet Airways Business', 'Vistara Premium economy',
#         'Trujet']

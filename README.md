<h2 align="center">Envisioning Yellow Taxi High Demand Areas in NYC city</h2>
<p align="center">
<img align="center" src="https://github.com/ssrbazpur/Envisioning-Yellow-Taxi-High-Demand-Areas-in-NYC-city/blob/master/Screenshots/nyc%20taxi.jpg?raw=true"/></p>
  </center>

<p align="justify">New York City is known as the home of the great yellow taxis. Yellow taxi cabs are the main vehicles that reserve the privilege of street-hailing and prearranged passengers anyplace in NYC. The vehicles that come under TLC (Taxi and Limousine Commission) includes yellow taxis, FHV’s(For-hire vehicles), Green cabs, Paratransit Vehicle and Commuter Vans. Yellow cab is the most iconic as they are allowed to pick the passenger waving for a ride anywhere in the city. Whereas FHV provides only pre-arranged services and Green Taxi permits street hailing but is restricted to some zones only in NYC city.</p>


<h3> Solution </h3>
<ol>
  <li>
I discovered the data from the TLC taxi trip website and then I retrieved the data from the AWS S3 bucket and stored all the data on Google Cloud Platform using Spark and Pandas.</li>
  <li>
I made Use of Big Query to analyze the data set and get only relevant rows from the dataset. I also made use of Big Query and pandas data frame to clean the data as well.</li>
  <li>
Carry out data exploration to find out the most demanding areas in NYC City and also to know how weather affects the count of NYC yellow taxi trips in NYC City.</li>
  <li>
Did Feature Engineering to get an effective outcome. Use methods like One hot encoding and binning in feature engineering.</li>
  <li>
    
 Divided my data set into train and test and also used cross-validation to get the optimal result from the model. The model used are ARIMA, Xgboot, Random Forest Regression, Linear Regression, Light GBM, etc. I used the Grid Search CV to get the best result from all the models shown above.</li>
<li>
Published a fully functional website using Flask that enables the yellow cab taxi drivers and TLC business to leverage the website to enhance their profit.</li>
<li>
Prepared Dashboard that can help the business know the weekly pickups in advance.</li>
</ol>



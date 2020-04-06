<h2 align="center">Envisioning Yellow Taxi High Demand Areas in NYC city</h2>
<p align="center">
  
<img width=400 height=400 src="https://cdn.lowgif.com/small/30eda5679770f2f2-gif-porco-rosso-animated-gif-on-gifer-by-conjuris.gif"/> </p>
<img align="center" src="https://github.com/ssrbazpur/Envisioning-Yellow-Taxi-High-Demand-Areas-in-NYC-city/blob/master/Screenshots/nyc%20taxi.jpg?raw=true"/></p>
  </center>
<h3> Introduction</h3>
<p align="justify">A unique quality about Yellow cabs is that they can pick up passengers from the streets without any pre-arranged booking required. Whereas in the case of Uber, passengers mainly use the app to arrange for the taxi. So I found a business opportunity for yellow cabs to get back on track by targeting the streets where the pickups demand are high. If the passenger waits too much they switch to apps to look for a taxi but if the passengers can see a yellow cab right in front of them, they will surely choose the yellow cab instead of waiting for Uber. Hence this data science projects focus to help the NYC TLC yellow taxis to get back on track and increase the number of pickups
around the NYC city. Also, the yellow cab taxi drivers can make use of the website to see the forecasted demand for different zones in NYC city.</p>


<h3> Data Analytics Lifecycle </h3>
<ol> <li> <a href="">Data Discovery</a> </li>
  <li> Data Preparation </li>
  <li> Model Planning </li>
  <li> Model Building </li>
  <li> Operationalize </li>
  <li> Communication </li>
  </ol>
    

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



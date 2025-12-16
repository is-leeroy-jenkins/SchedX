'''
  ******************************************************************************************
      Assembly:                Schedule-X
      Filename:                app.py
      Author:                  Terry D. Eppler
      Created:                 05-31-2022

      Last Modified By:        Terry D. Eppler
      Last Modified On:        05-01-2025
  ******************************************************************************************
  <copyright file='app.py' company='Terry D. Eppler'>

	     app.py
	     Copyright ©  2022  Terry Eppler

     Permission is hereby granted, free of charge, to any person obtaining a copy
     of this software and associated documentation files (the “Software”),
     to deal in the Software without restriction,
     including without limitation the rights to use,
     copy, modify, merge, publish, distribute, sublicense,
     and/or sell copies of the Software,
     and to permit persons to whom the Software is furnished to do so,
     subject to the following conditions:

     The above copyright notice and this permission notice shall be included in all
     copies or substantial portions of the Software.

     THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
     INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
     FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT.
     IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
     DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
     ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
     DEALINGS IN THE SOFTWARE.

     You can contact me at:  terryeppler@gmail.com or eppler.terry@epa.gov

  </copyright>
  <summary>
    app.py
  </summary>
  ******************************************************************************************
'''
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from plotly import graph_objs as go
from sklearn.linear_model import LinearRegression
import numpy as np

data = pd.read_csv( "stores/Salary_Data.csv" )
x = np.array( data[ 'YearsExperience' ] ).reshape( -1, 1 )
lr = LinearRegression( )
lr.fit( x, np.array( data[ 'Salary' ] ) )

st.title( "Schedule-X" )
st.image( "stores//sal.jpg", width=800 )
nav = st.sidebar.radio( "Navigation", [ "Home", "Prediction", "Contribute" ] )
if nav == "Home":
	if st.checkbox( "Show Table" ):
		st.table( data )
	
	graph = st.selectbox( "What kind of Graph?", [ "Non-Interactive", "Interactive" ] )
	
	val = st.slider( "Filter data using years", 0, 20 )
	data = data.loc[ data[ "YearsExperience" ] >= val ]
	if graph == "Non-Interactive":
		plt.figure( figsize=(10, 5) )
		plt.scatter( data[ "YearsExperience" ], data[ "Salary" ] )
		plt.ylim( 0 )
		plt.xlabel( "Years of Experience" )
		plt.ylabel( "Salary" )
		plt.tight_layout( )
		st.pyplot( )
	if graph == "Interactive":
		layout = go.Layout( xaxis=dict( range=[ 0, 16 ] ), yaxis=dict( range=[ 0, 210000 ] ) )
		fig = go.Figure( data=go.Scatter( x=data[ "YearsExperience" ], y=data[ "Salary" ], mode='markers' ), layout=layout )
		st.plotly_chart( fig )

if nav == "Prediction":
	st.header( "Know your Salary" )
	val = st.number_input( "Enter you exp", 0.00, 20.00, step=0.25 )
	val = np.array( val ).reshape( 1, -1 )
	pred = lr.predict( val )[ 0 ]
	
	if st.button( "Predict" ):
		st.success( f"Your predicted salary is {round( pred )}" )

if nav == "Contribute":
	st.header( "Contribute to our dataset" )
	ex = st.number_input( "Enter your Experience", 0.0, 20.0 )
	sal = st.number_input( "Enter your Salary", 0.00, 1000000.00, step=1000.0 )
	if st.button( "submit" ):
		to_add = \
		{
			"YearsExperience": [ ex ],
			"Salary": [ sal ]
		}
		to_add = pd.DataFrame( to_add )
		to_add.to_csv( "stores//Salary_Data.csv", mode='a', header=False, index=False )
		st.success( "Submitted" )

import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import altair as alt
from PIL import Image
import matplotlib as mpl
import matplotlib.pyplot as plt
from ggplot import *
import plotly.figure_factory as ff
import plotly.express as px
import plotly.offline as py
from plotnine import ggplot, aes, geom_line
from plotnine import *
from plotnine.data import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots
py.init_notebook_mode(connected=False)
st.set_option('deprecation.showPyplotGlobalUse', False)

#st.set_option('wideMode', True)
st.set_page_config(  # Alternate names: setup_page, page, layout
	layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
	page_title=None,  # String or None. Strings get appended with "• Streamlit". 
	page_icon=None,  # String, anything supported by st.image, or None.
)

password = st.sidebar.text_input('Enter your password',type="password")

if password == "Dashkhaj":

	st.sidebar.title("Heart Disease Dashbaords")
	st.sidebar.markdown("This application contains several dashboards related to Heart Disease data.")
	st.sidebar.markdown("The dataset contains 301 observations.")

	select = st.sidebar.selectbox('Select your dashboard',['About the Disease','General Overview','Factors'])

	image = Image.open('Heart Disease1.jpg')

	df = pd.read_csv('Heart Disease.csv')

	df["target"].replace({0: False, 1: True}, inplace=True)
	df["sex"].replace({0: "Female", 1: "Male"}, inplace=True)
	df["cp"].replace({0: "Asymptomatic", 1: "Atypical Angina",2: "Pain Without Relation to Angina", 3: "Typical Angina"}, inplace=True)
	df["fbs"].replace({0: "No", 1: "Yes"}, inplace=True)
	df["restecg"].replace({0: "Probable Left Ventricular Hypertrophy", 1: "Normal",2: "Abnormalities in the T Wave or ST Segment"}, inplace=True)
	df["exang"].replace({0: "No", 1: "Yes"}, inplace=True)
	df["slope"].replace({0: "Descending", 1: "Flat", 2: "Ascending"}, inplace=True)
	df.drop(df.loc[df['thal'] == 0].index, inplace=True)
	df["thal"].replace({1: "Fixed Defect", 2: "Normal Blood Flow",3: "Reversible Defect"}, inplace=True)
	df = df.rename(columns={'age': 'Age', 'sex': 'Sex', 'cp': 'Chest Pain', 'trestbps': 'RBP','chol': 'Cholesterol', 'fbs': 'Fasting Blood Sugar', 'exang': 'Angina','slope': 'Slope', 'target': 'Disease'})

	df_male = df[df['Sex']=="Male"]
	df_female = df[df['Sex']=="Female"]

	if select == "About the Disease":
		st.markdown("<h1 style='text-align: center; color: black;'>What is Heart Disease?</h1>", unsafe_allow_html=True)
		st.title(" ")

		c1,c2 = st.beta_columns(2)
		c1.image(image,width=560)
		#st.image(image,width=500)
		c2.markdown("Cardiovascular diseases (CVDs) are the number 1 cause of death globally, taking each year an estimated")
		c2.markdown("<h1 style='text-align: center; color: black;'>17.9 million lives", unsafe_allow_html=True)
		st.markdown("Cardiovascular disease, or CVD, is a very serious health condition that keeps the heart or blood vessels from working properly.") 	
		st.markdown("When our heart and blood vessels are working at their best, blood flows easily and is circulated around the body freely.")
		st.markdown("If there is a clog in our blood vessels or if our heart is not pumping blood properly, this prevents blood from being delivered to many important parts of our body. Not having blood constantly delivered throughout our body can cause serious illness or even death.")
		st.markdown("Although some people are born with certain types of CVD, most people develop CVD as a result of poor lifestyle habits, such as eating unhealthy foods, not getting enough exercise or using tobacco.")


	if select == "General Overview":
		

			st.markdown("<h1 style='text-align: center; color: black;'>General Overview of The Data</h1>", unsafe_allow_html=True)

			c1,c2,c3 = st.beta_columns(3)

			with c3:
				fig1 = px.histogram(df, x="Age",color="Disease",nbins=50, title = "Disease by Age")
				fig1.update_layout(
				title_x=0.5,
		    	autosize=False,
		    	width=480,
		    	height=430,
		    	yaxis={'visible': True, 'showticklabels': True})
				st.plotly_chart(fig1)

			with c1:
				fig2 = px.histogram(df, x='Sex', color="Disease", barmode='group', title = "Disease by Gender")
				fig2.update_layout(
				title_x=0.5,
		    	autosize=False,
		    	width = 380,
		    	height=430,
		    	showlegend=False,
		    	yaxis={'visible': True, 'showticklabels': True})
				st.plotly_chart(fig2)

			with c2:
				dis_false = df['Disease'].value_counts()[0]
				dis_true = df['Disease'].value_counts()[1]
				distr = [dis_false,dis_true]
				distr_n = ["False", "True"]
				fig3 = go.Figure(data=[go.Pie(labels=distr_n, values=distr, hole=.3)]) 
				fig3.update_layout(
				title='Distribution of the Disease',
				title_x=0.5,
		    	autosize=False,
		    	width = 400,
		    	height=430,
		    	showlegend=False)
				st.plotly_chart(fig3)

			c3, c4 = st.beta_columns(2)
			with c3:
				fig3 = px.scatter(df, x="Age", y="RBP", color="Disease", title="Disease by Resting Blood Pressure and Age")
				fig3.update_layout(
				title_x=0.5,
				width = 620,
				height = 400)
				st.plotly_chart(fig3)

			with c4:
				fig4 = px.histogram(df, x='Chest Pain', color="Sex", barmode='group',title="Chest Pain Types Distribution by Gender")
				fig4.update_layout(
				title_x=0.5,
				width = 620,
				height = 470)
				st.plotly_chart(fig4)


	if select == "Factors":

			gender = st.sidebar.selectbox('Select the gender',['All','Male','Female'])

			if gender == "All":
				st.markdown("<h1 style='text-align: center; color: black;'>Critical Factors</h1>", unsafe_allow_html=True)

				c1,c2,c3 = st.beta_columns(3)

				with c2:
					fig1 = px.box(df, x="Disease", y="thalach", title="Effect of Max Heart Rate During Exercise",
							labels={"thalach": "Max Heart Rate"}, color="Disease")
					fig1.update_layout(
					title_x=0.5,
					width = 400,
					height = 470)
					st.plotly_chart(fig1)

				with c1:
					fig2 = px.histogram(df, x='Chest Pain', color="Disease", barmode='group', title="Effect of Chest Pain")
					fig2.update_layout(
					title_x=0.5,
					width = 400,
					height = 470,
					showlegend=False)
					st.plotly_chart(fig2)

				with c3:
					fig3 = px.histogram(df, x='Angina', color="Disease", barmode='relative', title = "Effect of Angina")
					fig3.update_layout(
					title_x=0.5,
					width = 450,
					height = 470)
					st.plotly_chart(fig3)

				c4,c5 = st.beta_columns(2)
				with c4:
					labels = ["True","False"]

					# Create subplots: use 'domain' type for Pie subplot
					fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'},{'type':'domain'}]])
					fig.add_trace(go.Pie(labels=labels, values=[35,106], name="Ascending"),
					              1, 1)
					fig.add_trace(go.Pie(labels=labels, values=[12,9], name="Ascending"),
					              1, 2)
					fig.add_trace(go.Pie(labels=labels, values=[90,49], name="Flat"),
					              1, 3)


					# Use `hole` to create a donut-like pie chart
					fig.update_traces(hole=.5, hoverinfo="label+percent+name")

					fig.update_layout(
					    title_text="Effect of Slope",
					    title_x = 0.5,
					    # Add annotations in the center of the donut pies.
					    annotations=[dict(text='Ascending', x=0.075, y=0.5, font_size=12, showarrow=False),
					                 dict(text='Descending', x=0.5, y=0.5, font_size=10.5, showarrow=False),
					                 dict(text='Flat', x=0.88, y=0.5, font_size=13, showarrow=False)])
					st.plotly_chart(fig)

				with c5:
					fig5 = px.scatter(df, x="Age", y="Cholesterol", color="Disease", title="Disease by Cholesterol Level and Age")
					fig5.update_layout(
					title_x=0.5,
					width = 620,
					height = 400)
					st.plotly_chart(fig5)

			if gender == "Male":
				st.markdown("<h1 style='text-align: center; color: black;'>Critical Factors - Male</h1>", unsafe_allow_html=True)		
				c1,c2,c3 = st.beta_columns(3)

				with c1:
					fig1 = px.box(df_male, x="Disease", y="thalach", title="Effect of Max Heart Rate During Exercise",
							labels={"thalach": "Max Heart Rate"}, color="Disease")
					fig1.update_layout(
					title_x=0.5,
					width = 400,
					height = 470)
					st.plotly_chart(fig1)

				with c2:
					fig2 = px.histogram(df_male, x='Chest Pain', color="Disease", barmode='group', title="Effect of Chest Pain")
					fig2.update_layout(
					title_x=0.5,
					width = 400,
					height = 470,
					showlegend=False)
					st.plotly_chart(fig2)

				with c3:
					fig3 = px.histogram(df_male, x='Angina', color="Disease", barmode='relative', title = "Effect of Angina")
					fig3.update_layout(
					title_x=0.5,
					width = 450,
					height = 470)
					st.plotly_chart(fig3)

				c4,c5 = st.beta_columns(2)

				with c4:

					labels = ["True","False"]

					# Create subplots: use 'domain' type for Pie subplot
					fig5 = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'},{'type':'domain'}]])
					fig5.add_trace(go.Pie(labels=labels, values=[33,63], name="Ascending"),
					              1, 1)
					fig5.add_trace(go.Pie(labels=labels, values=[9,7], name="Descending"),
					              1, 2)
					fig5.add_trace(go.Pie(labels=labels, values=[71,23], name="Flat"),
					              1, 3)


					# Use `hole` to create a donut-like pie chart
					fig5.update_traces(hole=.5, hoverinfo="label+percent+name")

					fig5.update_layout(
					    title_text="Effect of Slope",
					    title_x = 0.5,
					    # Add annotations in the center of the donut pies.
					    annotations=[dict(text='Ascending', x=0.075, y=0.5, font_size=12, showarrow=False),
					                 dict(text='Descending', x=0.5, y=0.5, font_size=10.5, showarrow=False),
					                 dict(text='Flat', x=0.89, y=0.5, font_size=13, showarrow=False)])
					st.plotly_chart(fig5)

				with c5:
					fig6 = px.scatter(df_male, x="Age", y="Cholesterol", color="Disease", title="Disease by Cholesterol Level and Age")
					fig6.update_layout(
					title_x=0.5,
					width = 620,
					height = 400)
					st.plotly_chart(fig6)				
					
			if gender == "Female":
				st.markdown("<h1 style='text-align: center; color: black;'>Critical Factors - Female</h1>", unsafe_allow_html=True)

				c1,c2,c3 = st.beta_columns(3)

				with c1:
					fig1 = px.box(df_female, x="Disease", y="thalach", title="Effect of Max Heart Rate During Exercise",
							labels={"thalach": "Max Heart Rate"}, color="Disease")
					fig1.update_layout(
					title_x=0.5,
					width = 400,
					height = 470)
					st.plotly_chart(fig1)

				with c2:
					fig2 = px.histogram(df_female, x='Chest Pain', color="Disease", barmode='group', title="Effect of Chest Pain")
					fig2.update_layout(
					title_x=0.5,
					width = 400,
					height = 470,
					showlegend=False)
					st.plotly_chart(fig2)

				with c3:
					fig3 = px.histogram(df_female, x='Angina', color="Disease", barmode='relative', title = "Effect of Angina")
					fig3.update_layout(
					title_x=0.5,
					width = 450,
					height = 470)
					st.plotly_chart(fig3)

				c4,c5 = st.beta_columns(2)

				with c4:

					labels = ["True","False"]

					# Create subplots: use 'domain' type for Pie subplot
					fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'},{'type':'domain'}]])
					fig.add_trace(go.Pie(labels=labels, values=[2,43], name="Ascending"),
					              1, 1)
					fig.add_trace(go.Pie(labels=labels, values=[3,2], name="Descending"),
					              1, 2)
					fig.add_trace(go.Pie(labels=labels, values=[19,26], name="Flat"),
					              1, 3)


					# Use `hole` to create a donut-like pie chart
					fig.update_traces(hole=.5, hoverinfo="label+percent+name")

					fig.update_layout(
					    title_text="Effect of Slope",
					    title_x = 0.5,
					    # Add annotations in the center of the donut pies.
					    annotations=[dict(text='Ascending', x=0.07, y=0.5, font_size=12, showarrow=False),
					                 dict(text='Descending', x=0.5, y=0.5, font_size=10.5, showarrow=False),
					                 dict(text='Flat', x=0.89, y=0.5, font_size=13, showarrow=False)])

					st.plotly_chart(fig)

				with c5:
					fig6 = px.scatter(df_female, x="Age", y="Cholesterol", color="Disease", title="Disease by Cholesterol Level and Age")
					fig6.update_layout(
					title_x=0.5,
					width = 620,
					height = 400)
					st.plotly_chart(fig6)				

else:
	col1,col2 = st.beta_columns(2)
	
	with col1:
		st.image("heart disease.jpg",width = 500)
	
	with col2:
		st.title(" ")
		st.title(" ")
		st.title("Heart Disease Dashboard")
	
	st.write("You cannot access the dashboard without the password. Please contact Khajag Tabakian to obtain the password.")


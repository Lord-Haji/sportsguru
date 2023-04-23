import streamlit as st
import pickle
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="SportsGuru - IPL",
    page_icon="🏏"
    # layout="wide",
    # initial_sidebar_state="expanded",
)

teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Punjab Kings',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals'
#  'Gujarat Titans',
#  'Lucknow Supergiants'
 ]

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
       'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
       'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Sharjah', 'Mohali', 'Bengaluru']

pipe = pickle.load(open('pipe.pkl','rb'))
st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

# Sidebar implementation
# with st.sidebar:
#     batting_team = st.selectbox('Select the batting team', sorted(teams))
#     bowling_team = st.selectbox('Select the bowling team', sorted([team for team in teams if team != batting_team]))
#     selected_city = st.selectbox('Select host city', sorted(cities))
#     target = st.number_input('Target', step=1)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))

with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted([team for team in teams if team != batting_team]))
    


if batting_team == bowling_team:
    st.error("Please select different teams for batting and bowling")
else:

    selected_city = st.selectbox('Select host city', sorted(cities))
    target = st.number_input('Target', step=1)
    
    col3,col4,col5 = st.columns(3)
    
    with col3:
        score = st.number_input('Score', step=1, max_value=target-1 if target > 0 else None)
    with col4:
        overs = st.number_input('Overs completed', step=1, min_value=1, max_value=19)
    with col5:
        wickets = st.number_input('Wickets down', step=1, min_value=0, max_value=9)

    if st.button('Predict Probability'):
        runs_left = target - score
        balls_left = 120 - (overs*6)
        crr = score/overs
        rrr = (runs_left*6)/balls_left
        predicted_score = score + int(crr*balls_left/6)
        
        wickets = 10 - wickets

        input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets':[wickets],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})

        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]
        st.header("Win Probability:")
        col1, col2 = st.columns(2)
        with col1:
            st.write(batting_team + ": {:.2f}%".format(win*100))
        with col2:
            st.write(bowling_team + ": {:.2f}%".format(loss*100))
        
        st.header("Score Predictions:")
        st.write("CRR (Current Run Rate): {:.2f}".format(crr))
        st.write("RRR (Required Run Rate): {:.2f}".format(rrr))
        st.write("Predicted Score: {}".format(predicted_score), "/", str(10 - wickets))
        

        
        
# Footer implementation
current_year = date.today().year

footer = """
---
<div style='text-align: center; font-size: 14px; color: #888;'>
  <p>Powered by SportsGuru &mdash; IPL Win Predictor</p>
  <p>&copy; {} &mdash; Developed by <a href="https://github.com/lord-haji">lord-haji</a> and <a href="https://github.com/cs-sohan">cs-sohan</a></p>
</div>
""".format(current_year)

st.markdown(footer, unsafe_allow_html=True)

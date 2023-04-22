import streamlit as st
import pickle
import pandas as pd

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

# col1, col2 = st.columns(2)

with st.sidebar:
    batting_team = st.selectbox('Select the batting team', sorted(teams))
    bowling_team = st.selectbox('Select the bowling team', sorted([team for team in teams if team != batting_team]))
    selected_city = st.selectbox('Select host city', sorted(cities))
    target = st.number_input('Target', step=1)


if batting_team == bowling_team:
    st.error("Please select different teams for batting and bowling")
else:

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
        wickets = 10 - wickets
        crr = score/overs
        rrr = (runs_left*6)/balls_left

        input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets':[wickets],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})

        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]
        st.header(batting_team + "- " + str(round(win*100, 2)) + "%")
        st.header(bowling_team + "- " + str(round(loss*100, 2)) + "%")

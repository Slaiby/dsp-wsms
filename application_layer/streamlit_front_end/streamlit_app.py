import os
import streamlit as st
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

st.set_page_config(page_title='House Prices Prediction', page_icon='🏠', layout='wide', initial_sidebar_state='auto')

header = st.container()
dataset = st.container()
features = st.container()
modelTraining = st.container()



# # Custom CSS
# custom_styles = """
# <style>
#     .main {
#         background-color: #f5f5f5;
#         color: grey;
#     }
#     .title-text {
#         color: green;
#     }
# </style>
# """

# # Apply the custom styles using st.markdown
# st.markdown(custom_styles, unsafe_allow_html=True)


@st.cache_data
def get_data(filename):

    house_data = pd.read_csv(filename)
    return house_data

with header:
    st.title('Welcome to my awesome data science project!')
    st.text('In this project, I look into the House pricing modeling')

with dataset:
    st.header('House Prices Dataset')
    st.text('I found this dataset on Kaggle and it contains information about the House prices.')

    house_data = get_data(os.getcwd()+ '/logic_layer/data/test.csv')
    st.write(house_data.head())

    st.subheader('LotArea distribution')
    street_dist = pd.DataFrame(house_data['LotArea'].value_counts())
    st.bar_chart(street_dist) 


with features:
    st.header('The features')

    st.markdown('**This is a first feature**')


with modelTraining:
    # house_data_encoded = pd.get_dummies(house_data, columns=['Street'], drop_first=True)

    st.header('Time to train the model')
    st.text('Here you get to choose the hyperparameters of the model and see how the performance changes')

    sel_col, disp_col = st.columns(2)

    max_depth = sel_col.slider('Select the max depth of the model', min_value=10, max_value=100, value=20, step=10)

    n_estimators = sel_col.selectbox('Select the number of trees in the forest', options=[100, 200, 300, 'No limit'], index=0)

    sel_col.text('List of features: ')
    sel_col.write(house_data.columns) 

    input_feature = sel_col.text_input('Enter the feature you want to use to train the model', 'LotArea')

    # regres = RandomForestRegressor(max_depth=max_depth, n_estimators=n_estimators)

    # X = house_data_encoded.drop('LotArea', axis=1)  # Drop the target variable
    # y = house_data_encoded['LotArea']

    # regres.fit(X, y)
    # prediction = regres.predict(X)

    # disp_col.subheader('Mean absolute error of the model is:')
    # disp_col.write(mean_absolute_error(y, prediction))

    # disp_col.subheader('Mean squared error of the model is:')
    # disp_col.write(mean_squared_error(y, prediction))

    # disp_col.subheader('R squared score of the model is:')
    # disp_col.write(r2_score(y, prediction))

    house_data_encoded = pd.get_dummies(house_data, drop_first=True)

    # Impute missing values
    imputer = SimpleImputer(strategy='mean')
    X_imputed = imputer.fit_transform(house_data_encoded.drop('LotArea', axis=1))  # Drop the target variable
    y = house_data_encoded['LotArea']

    if n_estimators == 'No limit':
        regres = RandomForestRegressor(max_depth=max_depth)

    else:
        regres = RandomForestRegressor(max_depth=max_depth, n_estimators=n_estimators)
        
    # Train the model
    
    regres.fit(X_imputed, y)

    # Predictions
    prediction = regres.predict(X_imputed)

    # Evaluation metrics
    disp_col.subheader('Mean absolute error of the model is:')
    disp_col.write(mean_absolute_error(y, prediction))

    disp_col.subheader('Mean squared error of the model is:')
    disp_col.write(mean_squared_error(y, prediction))

    disp_col.subheader('R squared score of the model is:')
    disp_col.write(r2_score(y, prediction))

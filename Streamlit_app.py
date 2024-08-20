import streamlit as st
import pandas as pd
import joblib

# Load the trained machine learning model
predicted_model = joblib.load('lasso_model.pkl')

# Load the dataset
df = pd.read_csv('car_price_prediction_edit.csv')

# Grouping and preparing dictionaries
model_dict = df.groupby('Manufacturer')['Model'].unique().to_dict()
category_dict = df.groupby('Model')['Category'].unique().to_dict()
fuel_type_dict = df.groupby('Category')['Fuel_type'].unique().to_dict()
gear_type_dict = df.groupby('Category')['Gear_type'].unique().to_dict()

# Convert numpy arrays to lists for better compatibility
for dictionary in [model_dict, category_dict, fuel_type_dict, gear_type_dict]:
    for key, value in dictionary.items():
        dictionary[key] = list(value)

# Streamlit UI
def main():
    st.title("Car Price Prediction")

    # Sidebar with feature input
    st.sidebar.header("Input Features")

    # Manufacturer Selection
    manufacturer = st.sidebar.selectbox("Manufacturer", df['Manufacturer'].unique())

    # Based on Manufacturer, display the Models
    model = st.sidebar.selectbox("Model", model_dict[manufacturer])

    # Based on Model, display the Categories
    category = st.sidebar.selectbox("Category", category_dict[model])

    # Based on Category, display the Fuel Types and Gear Types
    fuel_type = st.sidebar.selectbox("Fuel Type", fuel_type_dict[category])
    gear_type = st.sidebar.selectbox("Gear Type", gear_type_dict[category])

    produced_year = st.sidebar.slider("Produced Year", min_value=2000, max_value=2023, value=2010, step=1)

    # Displaying the user input for Streamlit view
    display_data = {
        'Manufacturer': manufacturer,
        'Model': model,
        'Produced Year': f"{produced_year}",  # Display without comma
        'Category': category,
        'Fuel Type': fuel_type,
        'Gear Type': gear_type
    }
    st.subheader("User Input Features")
    st.write(pd.DataFrame([display_data]))

    # Prepare the data for prediction
    data_for_prediction = {
        'Manufacturer': [manufacturer],
        'Model': [model],
        'Produced_year': [produced_year],  # Ensure the column names match with training data
        'Category': [category],
        'Fuel_type': [fuel_type],
        'Gear_type': [gear_type]
    }

    # Predict the price
    try:
        predicted_price = predicted_model.predict(pd.DataFrame(data_for_prediction))
        st.subheader('Predicted Price')
        st.success("The estimated price of your car is ${}. ".format(int(predicted_price[0])))
    except Exception as e:
        st.error(f"Error during prediction: {e}")
        
if __name__ == '__main__':
    main()

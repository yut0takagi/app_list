import pandas as pd
from plotly import graph_objs

def main():
    # Input temperature data
    df = pd.DataFrame(columns=['Temperature (°C)', 'Temperature (°F)'])
    
    # Create input form
    print("Enter temperature in Celsius:")
    celsius = float(input())
    
    # Convert to Fahrenheit
    fahrenheit = celsius * 9/5 + 32
    
    # Add data to DataFrame
    df.loc[0] = [celsius, fahrenheit]
    
    # Plot data
    fig = graph_objs.Figure(data=[graph_objs.Scatter(x=df['Temperature (°C)'], y=df['Temperature (°F)'])])
    fig.show()

if __name__ == '__main__':
    main()

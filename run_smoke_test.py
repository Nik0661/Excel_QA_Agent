"""Quick smoke test to verify imports and data loading."""
from agent_app.loader import load_data


def main():
    df_sales, df_forecast = load_data()
    print("Sales loaded:", df_sales is not None)
    print("Forecast loaded:", df_forecast is not None)

if __name__ == '__main__':
    main()

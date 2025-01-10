import os
import pandas as pd
import matplotlib.pyplot as plt

def aggregate_views_by_date(results_folder="results", chart_output="views_chart.png"):
    """
    Reads Excel files from the results folder, aggregates views by date, and plots a chart.
    Ensures every day is displayed on the x-axis, even if there are no views.
    """
    # Check if results folder exists
    if not os.path.exists(results_folder):
        print(f"Folder '{results_folder}' does not exist.")
        return

    # List all Excel files in the results folder
    excel_files = [f for f in os.listdir(results_folder) if f.endswith(".xlsx")]

    if not excel_files:
        print(f"No Excel files found in the '{results_folder}' folder.")
        return

    # DataFrame to store combined data
    combined_data = pd.DataFrame()

    for excel_file in excel_files:
        file_path = os.path.join(results_folder, excel_file)
        print(f"Processing file: {file_path}")

        try:
            # Read the Excel file
            df = pd.read_excel(file_path)

            # Log available columns and preview data
            print(f"Columns in {file_path}: {df.columns.tolist()}")
            print(f"Preview of data in {file_path}:")
            print(df[['upload_date', 'view_count']].head())

            # Ensure required columns exist
            if 'upload_date' not in df.columns or 'view_count' not in df.columns:
                print(f"Skipping '{file_path}' as it does not contain required columns.")
                continue

            # Convert upload_date from YYYYDDMM to standard datetime format
            df['upload_date'] = pd.to_datetime(df['upload_date'], format='%Y%d%m', errors='coerce')

            # Drop rows with invalid dates or missing views
            df = df.dropna(subset=['upload_date', 'view_count'])

            # Ensure view_count is numeric
            df['view_count'] = pd.to_numeric(df['view_count'], errors='coerce')
            df = df.dropna(subset=['view_count'])

            # Append to combined data
            combined_data = pd.concat([combined_data, df[['upload_date', 'view_count']]])

        except Exception as e:
            print(f"Error processing file '{file_path}': {e}")

    if combined_data.empty:
        print("No valid data found in the provided Excel files.")
        return

    # Rename columns for consistency
    combined_data.columns = ['date', 'views']

    # Aggregate views by date
    aggregated_data = combined_data.groupby('date')['views'].sum().reset_index()

    # Sort by date
    aggregated_data = aggregated_data.sort_values(by='date')

    # Ensure all days are included on the x-axis
    full_date_range = pd.date_range(start=aggregated_data['date'].min(), end=aggregated_data['date'].max())
    aggregated_data = aggregated_data.set_index('date').reindex(full_date_range, fill_value=0).reset_index()
    aggregated_data.columns = ['date', 'views']

    # Plot the chart
    plt.figure(figsize=(12, 6))
    plt.plot(aggregated_data['date'], aggregated_data['views'], marker='o', linestyle='-', label='Views')
    plt.title("Views Over Time")
    plt.xlabel("Date")
    plt.ylabel("Total Views")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Save the chart
    plt.savefig(chart_output)
    print(f"Chart saved to: {chart_output}")

    # Show the chart
    plt.show()


if __name__ == "__main__":
    aggregate_views_by_date(results_folder="results", chart_output="views_chart.png")

import streamlit as st
import pandas as pd
import altair as alt

def main():
    st.title("CSV Transformer")
    
    # Step 1: Upload CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Original CSV File:")
        st.write(df)
        
        # Step 2: Clean data
        st.subheader("Clean Data")
        
        # Ask user for date column names and format
        date_columns = st.text_input("Enter date column names separated by commas (e.g., 'Date', 'Created Date')")
        date_format = st.text_input("Enter the desired date format (e.g., '%Y-%m-%d')")
        
        # Option to skip date standardization
        skip_date_standardization = st.checkbox("Skip Date Standardization")
        
        # Only show clean data button if user either skips date standardization or fills in date columns and format
        if skip_date_standardization or (date_columns and date_format):
            clean_data = st.button("Clean Data")
            
            if clean_data:
                original_df = df.copy()  # Keep a copy of the original dataframe for comparison
                
                # Convert all text to uppercase
                df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)
                # Uppercase all column names
                df.columns = df.columns.str.upper()
                # Remove duplicates
                df = df.drop_duplicates()
                # Correctly remove rows with any null value
                df = df.dropna()  # This removes rows with at least one null value
                
                # Standardize date columns if not skipped
                if not skip_date_standardization and date_columns:
                    for column in date_columns.split(','):
                        column = column.strip().upper()
                        if column in df.columns:
                            df[column] = pd.to_datetime(df[column]).dt.strftime(date_format)
                
                # Display data cleaning techniques to the user
                st.write("Data Cleaning Techniques Applied:")
                st.write("1. Converted all text to uppercase.")
                st.write("2. Uppercased all column names.")
                st.write("3. Removed duplicates.")
                st.write("4. Removed rows with at least one null value.")
                if not skip_date_standardization and date_columns:
                    st.write(f"5. Standardized date columns to format: {date_format}")
                
                # Identify rows removed due to null values
                null_removed_rows = original_df[original_df.isnull().any(axis=1)]  # Keep rows with nulls
                
                # Debugging output
                st.write("Rows removed due to null values:")
                st.write(null_removed_rows)  # Display the removed rows for debugging
                
                # Check if any rows were removed
                if not null_removed_rows.empty:
                    null_removed_rows['Reason'] = 'Null Value'
                    
                    # Download removed rows CSV if any rows were removed
                    removed_csv = null_removed_rows.to_csv(index=False)  # Added index=False for cleaner CSV
                    st.download_button(
                        label="Download Removed Rows",
                        data=removed_csv,
                        file_name="removed_rows.csv",
                        mime="text/csv"
                    )
                
                st.write("Transformed CSV File:")
                st.write(df)
                
                # Display mode for each column with a count of how many unique values per column and how many times the mode value appears
                mode_counts = df.mode().iloc[0]  # Get the first row of the mode DataFrame
                unique_counts = df.nunique().reset_index()  # Count unique values for each column and reset index
                unique_counts.columns = ['Column', 'Unique Values']  # Rename columns for clarity
                mode_value_counts = df.apply(lambda col: col.value_counts().max() if col.dtype == 'object' else None)  # Count the maximum occurrences of the mode value for each column
                
                st.write("Mode, Unique Value Counts, and Mode Value Counts per Column:")
                st.write(pd.DataFrame({'Mode': mode_counts, '# of Unique Field Values': unique_counts['Unique Values'], 'Mode Value Counts': mode_value_counts}))
                
                # Output the number of columns and rows in the final transformed data
                st.write(f"Number of Columns in Transformed Data: {len(df.columns)}")
                st.write(f"Number of Rows in Transformed Data: {len(df)}")
                
                # Visualizations
                st.subheader("Visualizations")
                
                # Plotting unique values per column
                unique_values_chart = alt.Chart(unique_counts, title='Unique Values per Column').mark_bar().encode(
                    x='Column',
                    y='Unique Values'
                ).properties(
                    width=600,
                    height=400
                )
                st.altair_chart(unique_values_chart)
                
                # Plotting mode value counts per column
                mode_value_counts_chart = alt.Chart(mode_value_counts.reset_index(), title='Mode Value Counts per Column').mark_bar().encode(
                    x='index',
                    y='Mode Value Counts'
                ).properties(
                    width=600,
                    height=400
                )
                st.altair_chart(mode_value_counts_chart)
                
                # Step 3: Download transformed CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Transformed CSV",
                    data=csv,
                    file_name="transformed_file.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
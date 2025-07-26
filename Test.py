# Test.py
def date_between(start_date, end_date):
    """
    Calculate the number of days between two dates.
    
    Parameters:
    start_date (str): The start date in 'YYYY-MM-DD' format.
    end_date (str): The end date in 'YYYY-MM-DD' format.
    
    Returns:
    int: The number of days between the two dates.
    """
    from datetime import datetime
    
    # Convert string dates to datetime objects
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Calculate the difference in days
    delta = end - start
    
    return delta.days

# Test the function
if __name__ == "__main__":
    # Example usage
    start_date = "2025-01-01"
    end_date = "2025-07-31"
    
    result = date_between(start_date, end_date)
    print(f"Days between {start_date} and {end_date}: {result}") 
# Function to calculate the number of days between two dates
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

    try:
        # Convert string dates to datetime objects
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError as e:
        raise ValueError("Dates must be in 'YYYY-MM-DD' format") from e

    # Calculate the difference in days
    if end < start:
        raise ValueError("End date must not be before start date")
    delta = end - start

    return delta.days

print(f"Test: {date_between('2025-01-01', '2025-07-31')} days")  # Example usage
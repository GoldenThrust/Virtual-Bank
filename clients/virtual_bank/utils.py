from django.utils import timezone

def calculate_time_difference_from_now(past_time):
    # Convert the past_time string to a timezone-aware datetime object
    past_datetime = timezone.make_aware(past_time)
    
    # Get the current time in the timezone
    current_datetime = timezone.now()
    
    # Calculate the time difference
    time_difference = current_datetime - past_datetime
    
    # Convert time difference to seconds
    total_seconds = time_difference.total_seconds()
    
    # Calculate years, months, weeks, days, hours, and minutes
    years = total_seconds // (365 * 24 * 3600)
    months = total_seconds // (30 * 24 * 3600)
    weeks = total_seconds // (7 * 24 * 3600)
    days = total_seconds // (24 * 3600)
    hours = total_seconds // 3600
    minutes = total_seconds // 60
    
    # Generate human-readable time difference string
    if years > 0:
        return f"{int(years)} {'year' if years == 1 else 'years'} ago"
    elif months > 0:
        return f"{int(months)} {'month' if months == 1 else 'months'} ago"
    elif weeks > 0:
        return f"{int(weeks)} {'week' if weeks == 1 else 'weeks'} ago"
    elif days > 0:
        return f"{int(days)} {'day' if days == 1 else 'days'} ago"
    elif hours > 0:
        return f"{int(hours)} {'hour' if hours == 1 else 'hours'} ago"
    elif minutes > 0:
        return f"{int(minutes)} {'minute' if minutes == 1 else 'minutes'} ago"
    else:
        return 'just now'

past_time = '2023-12-18 18:30:00'
time_ago = calculate_time_difference_from_now(past_time)
print(time_ago)

# import asyncio
# from datetime import datetime, timedelta
# from supabase import create_client, Client
# from dotenv import load_dotenv
# import  os
# load_dotenv()
# # Supabase connection details
# url: str = "https://wqlryzngdnfrarolbmma.supabase.co"
# # key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndxbHJ5em5nZG5mcmFyb2xibW1hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTc1MDk4NTksImV4cCI6MjAzMzA4NTg1OX0.zHkAeB9XxyC30WtQJSQnEyvNKCDneZ05EIQ6lfIHqQw"
# key: str=  os.getenv("supabase")
# supabase: Client = create_client(url, key)

# async def reset_user_attempts():
#     current_time = datetime.now()
#     print(current_time - timedelta(hours=24))
#     # current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
#     # Retrieve all users whose last_attempt_time is older than 24 hours
#     result = supabase.table('ielts_speaking_users').select('user_id').lt('last_attempt_time', current_time - timedelta(hours=24)).execute()
    
#     if result.data:
#         # Reset attempts_remaining for the eligible users
#         supabase.table('ielts_speaking_users').update({
#             'attempts_remaining': 5
#         }).in_('user_id', [user['user_id'] for user in result.data]).execute()
# async def main():
#     while True:
#         await reset_user_attempts()
        
#         print("number of attempts have updated")
#         await asyncio.sleep(3600)  # Sleep for 1 hour (3600 seconds)

# if __name__ == '__main__':
#     asyncio.run(main())

import asyncio
from datetime import datetime, timedelta
from supabase import create_client, Client
from dotenv import load_dotenv
from pytz import utc
import os
from flask import Flask
load_dotenv()
app = Flask(__name__)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200
# Supabase connection details
url: str = "https://wqlryzngdnfrarolbmma.supabase.co"
# key: str = os.getenv("supabase")
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndxbHJ5em5nZG5mcmFyb2xibW1hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTc1MDk4NTksImV4cCI6MjAzMzA4NTg1OX0.zHkAeB9XxyC30WtQJSQnEyvNKCDneZ05EIQ6lfIHqQw"

supabase: Client = create_client(url, key)

async def reset_user_attempts():
    current_time = datetime.now(utc)
    print(f"Resetting attempts at: {current_time}")
    
    # Log state of a few users before reset
    before_reset = supabase.table('ielts_speaking_users').select('*').limit(5).execute()
    print("State before reset:", before_reset.data)
    
    # Reset attempts_remaining for all users
    result = supabase.table('ielts_speaking_users').update({
        'attempts_remaining': 5,
        'last_attempt_time': current_time.isoformat()
    }).gte('user_id', 0).execute()  # This condition will apply to all rows with non-negative user_id
    
    # Log state of the same users after reset
    after_reset = supabase.table('ielts_speaking_users').select('*').limit(5).execute()
    # print("State after reset:", after_reset.data)
    
    print(f"Reset attempts for {len(result.data)} users")
async def main():
    while True:
        # Get the current time in UTC
        utc_time = datetime.now(utc)
        
        # Calculate the time until the next 21:00 in UTC
        next_reset_time = utc_time.replace(hour=21, minute=0, second=0, microsecond=0)
        if next_reset_time <= utc_time:
            next_reset_time += timedelta(days=1)
        time_until_reset = (next_reset_time - utc_time).total_seconds()
        
        print(f"Time until next reset at 21:00 UTC: {timedelta(seconds=time_until_reset)}")
        
        # Sleep until the next 21:00 in UTC
        await asyncio.sleep(time_until_reset)
        
        # Reset user attempts at 21:00 in UTC
        await reset_user_attempts()
        print("Number of attempts have been updated")

if __name__ == '__main__':
    from threading import Thread
    flask_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True)
    flask_thread.start()
    asyncio.run(main())

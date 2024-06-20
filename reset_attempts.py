# import asyncio
# from datetime import datetime, timedelta
# from supabase import create_client, Client
# from dotenv import load_dotenv
# import  os
# load_dotenv()
# # Supabase connection details
# url: str = "https://wqlryzngdnfrarolbmma.supabase.co"
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
load_dotenv()

# Supabase connection details
url: str = "https://wqlryzngdnfrarolbmma.supabase.co"
key: str=  os.getenv("supabase")
supabase: Client = create_client(url, key)

async def reset_user_attempts():
    current_time = datetime.now(utc)
    print(current_time - timedelta(hours=24))
    
    # Retrieve all users whose last_attempt_time is older than 24 hours
    result = supabase.table('ielts_speaking_users').select('user_id').lt('last_attempt_time', current_time - timedelta(hours=24)).execute()
    
    if result.data:
        # Reset attempts_remaining for the eligible users
        supabase.table('ielts_speaking_users').update({
            'attempts_remaining': 5
        }).in_('user_id', [user['user_id'] for user in result.data]).execute()

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
    asyncio.run(main())

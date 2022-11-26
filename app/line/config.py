import os
if os.getenv('API_ENV') != 'production':
    from dotenv import load_dotenv
    load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
API_ENV = os.getenv('API_ENV')

print("API_ENV : ",API_ENV)
print("ACCESS_TOKEN : ",LINE_CHANNEL_ACCESS_TOKEN)
print("CHANNEL_SECRET : ",LINE_CHANNEL_SECRET)

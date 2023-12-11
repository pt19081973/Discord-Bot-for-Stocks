import matplotlib.pyplot as plt
from io import BytesIO
import yfinance as yf
import discord
from datetime import datetime
from discord.ext import commands
import requests
from discord.ext.commands import has_permissions, MissingPermissions

TOKEN = "MTE3OTcxMTE2NzcwNzQ5MjQyMw.G_pP24.ekloXFhWOugQeej7iTXmLHeth3UPDL08IqZ8S8"
AV_API_KEY = "K4GK6P3OJS9WWSY2"

intents = discord.Intents.all()
intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')
    



@bot.command(name='stock')
async def stock(ctx, symbol):
    """Get stock information for a given symbol."""
    URL=f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={AV_API_KEY}"
    r = requests.get(URL)
    if r.status_code == 200:
        data = r.json()
        if 'Global Quote' in data:
            global_quote = data['Global Quote']
            stock_info_message = f"Stock Information for {symbol}:\n"
            for key, value in global_quote.items():
                stock_info_message += f"{key}: {value}\n"
            
            await ctx.send(stock_info_message)  # Sending the message to Discord
        else:
            await ctx.send("Error: Global Quote not found in the API response.")
    else:
        await ctx.send(f"Error: Unable to fetch data. Status code: {r.status_code}")
        
@bot.command(name='stock_trend')
async def stock_trend(ctx, symbol): 
    
    """Get stock information and plot last year's data."""
    URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={AV_API_KEY}"
    r = requests.get(URL)
    try:
        if r.status_code == 200:
            data = r.json()
            if 'Time Series (Daily)' in data:
                time_series = data['Time Series (Daily)']
                
                # Extracting data for the last year
                last_year_dates = list(time_series.keys())[:252]  # Assuming data is available for each business day
                last_year_dates.reverse()
                last_year_close_prices = [float(time_series[date]['4. close']) for date in last_year_dates]
                
                # Plotting the data
                plt.figure(figsize=(10,7))
                plt.plot(last_year_dates, last_year_close_prices, label='Closing Price')
                plt.title(f"Stock Data for {symbol}")
                plt.xlabel("Date")
                plt.ylabel("Closing Price")
                plt.xticks(last_year_dates[::9], rotation=45, ha="right")
                plt.legend()
                
                # Save the plot to a BytesIO object
                image_stream = BytesIO()
                plt.savefig(image_stream, format='png')
                plt.close()
                
                # Send the plot as an image
                image_stream.seek(0)
                await ctx.send(file=discord.File(image_stream, filename='stock_plot.png'))
            else:
                await ctx.send("Error: Time Series (Daily) not found in the API response.")
        else:
            await ctx.send(f"Error: Unable to fetch data. Status code: {r.status_code}")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        




















    
        
# The code `@bot.command(name='stock_trend')` is a decorator that defines a new command for the bot.
# The command is named "stock_trend" and can be invoked by users with the prefix "!".
# @bot.command(name='stock_trend')
# async def stock_trend(ctx, symbol):
#     """Get stock information and plot last year's data."""
#     stock_data = yf.download(symbol, start="2022-01-01", end="2023-01-01")
    
#     if not stock_data.empty:
#         last_year_dates = stock_data.index.strftime('%Y-%m-%d').tolist()
#         last_year_close_prices = stock_data['Close'].tolist()
        
#         # Plotting the data
#         plt.figure(figsize=(10, 6))
#         plt.plot(last_year_dates, last_year_close_prices, label='Closing Price')
#         plt.title(f"Stock Data for {symbol} - Last Year")
#         plt.xlabel("Date")
#         plt.ylabel("Closing Price")
        
#         # Customize x-axis ticks for better readability
#         plt.xticks(last_year_dates[::20], rotation=25, ha="right")
        
#         plt.legend()
        
#         # Save the plot to a BytesIO object
#         image_stream = BytesIO()
#         plt.savefig(image_stream, format='png')
#         plt.close()
        
#         # Send the plot as an image
#         image_stream.seek(0)
#         await ctx.send(file=discord.File(image_stream, filename='stock_plot.png'))
#     else:
#         await ctx.send(f"Error: Unable to fetch data for {symbol}")
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    # if r.status_code==200:
    #     data=r.json()
    #     if 'Global Quote' in data:
    #         global_quote = data['Global Quote']
    #         for key, value in global_quote.items():
    #             print(f"{key}: {value}")
    #     else:
    #         print("Error: Global Quote not found in the API response.")
    # else:
    #     print(f"Error: Unable to fetch data. Status code: {r.status_code}")
    
    
    
    
    
    # endpoint = 'https://www.alphavantage.co/query'
    # function = 'GLOBAL_QUOTE'
    
    # params = {
    #     'function': function,
    #     'symbol': symbol,
    #     'API_KEY': AV_API_KEY,
    # }


    # try:
    #     response = requests.get(endpoint, params=params)
    #     data = response.json()
    #     if 'GLOBAL_QUOTE' in data:
    #         stock_info = data['GLOBAL_QUOTE']
    #         embed = discord.Embed(
    #             title=f"Stock Information for {symbol}",
    #             description=f"Last Refreshed: {stock_info['07. Latest Trading Day']}",
    #             color=discord.Color.green(),
    #         )
    #         embed.add_field(name='Symbol', value=stock_info['01. symbol'], inline=True)
    #         embed.add_field(name='Open', value=stock_info['02. open'], inline=True)
    #         embed.add_field(name='High', value=stock_info['03. high'], inline=True)
    #         embed.add_field(name='Low', value=stock_info['04. low'], inline=True)
    #         embed.add_field(name='Price', value=stock_info['05. price'], inline=True)
    #         embed.add_field(name='Volume', value=stock_info['06. volume'], inline=True)
    #         await ctx.send(embed=embed)
    #     else:
    #         await ctx.send(f"Unable to fetch stock information for {symbol}")
    # except Exception as e:
    #     print(e)
    #     await ctx.send("An error occurred while fetching stock information.")

bot.run(TOKEN)


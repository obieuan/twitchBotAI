# ObiAI

ObiAI a Python based script to integrate your own bot to Twitch, bot is powered by ChatGPT and Twitchio libraries

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install libraries.

```bash
pip install twitchio
```
```bash
pip install openai
```

## Usage
First you will need to create a Twitch profile to be used as a bot.
Also you will have to get both Twitch and OpenAI API tokens

For twitch you can refer their [documentation](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/) or use [Twitch Chat OAuth Password Generator](https://twitchapps.com/tmi/)

For OpenAI you have to create an account and then get your own APItoken. [Visit their site](https://platform.openai.com/docs/introduction) for more information

Create a **config.py** file with the following code (or rename one provided) and replace the data with your own
```bash
# Twitch config
TWITCH_BOT_NAME = 'your_bot_id'          #This is the name of your bot
TWITCH_BOT_TOKEN = 'your_bot_token'      #Token looks like: Oauth:xxxxxxxxx

# OpenAI config
OPENAI_API_KEY = 'OpenAI_token'          #Looks something like: sk-xxxxxxxxxxxxxx

#Channels where you want to send your bot
CHANNELS = ['channel1', 'channel2', 'channel3'] #You can add as many as you want, just be careful to avoid spam

```
Once everything is properly configured, just run **ObiAI.py**
## Current Functions:
- Ability to interact with several users and remember last 10 conversations. 
- Ability to interact with several channels at the same time.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

ObiEuan
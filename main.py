import asyncio
import os

from steel import Steel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

from browser_use import Agent, BrowserConfig
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
	raise ValueError('GEMINI_API_KEY is not set')

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))


# MARK: Steel.dev
# Initialize Steel client with API key
client = Steel(steel_api_key="ste-GOGmYoH7m81VHiQzFtQ45JEl2diebDkxHrN39CnOPCgqCArIVm6zknmeAT0W6QZVAC1FWjm2jaVqe2uwRbmqDmh9XbqU4vQMznf")

# Create a Steel session
session = client.sessions.create()

print(f"View live session at: {session.session_viewer_url}")

cdp_url = f"wss://connect.steel.dev?apiKey=ste-GOGmYoH7m81VHiQzFtQ45JEl2diebDkxHrN39CnOPCgqCArIVm6zknmeAT0W6QZVAC1FWjm2jaVqe2uwRbmqDmh9XbqU4vQMznf&sessionId={session.id}"

browser = Browser(config=BrowserConfig(cdp_url=cdp_url))
browser_context = BrowserContext(browser=browser)

config = BrowserConfig(
    wss_url="wss://your-browser-provider.com/ws"
)

# Read prompt file
prompt = ""

with open('prompt.txt', 'r') as f:
	prompt = f.read()

print(prompt)

async def run_search():
	agent = Agent(
		task=prompt,
		llm=llm,
		max_actions_per_step=4,
		browser=browser,
		browser_context=browser_context,
	)

	await agent.run(max_steps=25)


if __name__ == '__main__':
	asyncio.run(run_search())

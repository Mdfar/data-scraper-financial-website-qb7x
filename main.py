import asyncio import pandas as pd from scraper.session_manager import FinancialScraper

async def main(): scraper = FinancialScraper(username="member@example.com", password="secure_password")

# Run once to set up session
if not os.path.exists("session.json"):
    await scraper.login_and_save_session()

# Scrape specific investment segments
trade_data = await scraper.scrape_historical_data("[https://www.verifiedinvesting.com/members/verified-trades](https://www.verifiedinvesting.com/members/verified-trades)")

# Organize into Excel
df = pd.DataFrame(trade_data)
df.to_excel("Verified_Investing_Report_2026.xlsx", index=False)
print("Data extraction complete. Report generated.")


if name == "main": asyncio.run(main())
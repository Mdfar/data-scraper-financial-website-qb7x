import json import os from playwright.async_api import async_playwright

class FinancialScraper: def init(self, username, password, session_path="session.json"): self.username = username self.password = password self.session_path = session_path self.url = "https://www.verifiedinvesting.com/login"

async def login_and_save_session(self):
    """Initial login to capture cookies and session state"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) # Headful for initial manual 2FA if needed
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto(self.url)
        await page.fill('input[name="email"]', self.username)
        await page.fill('input[name="password"]', self.password)
        await page.click('button[type="submit"]')
        
        # Wait for dashboard to confirm successful login
        await page.wait_for_selector(".dashboard-container", timeout=60000)
        
        # Save storage state
        await context.storage_state(path=self.session_path)
        await browser.close()
        print("Session saved successfully.")

async def scrape_historical_data(self, target_url):
    """Uses saved session to scrape members-only content"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=self.session_path)
        page = await context.new_page()
        
        await page.goto(target_url)
        await page.wait_for_load_state("networkidle")
        
        # Extracting trade table data
        data = await page.evaluate('''() => {
            const rows = Array.from(document.querySelectorAll('table.trades-table tr'));
            return rows.slice(1).map(row => {
                const cols = row.querySelectorAll('td');
                return {
                    date: cols[0]?.innerText,
                    ticker: cols[1]?.innerText,
                    action: cols[2]?.innerText,
                    price: cols[3]?.innerText,
                    profit_loss: cols[4]?.innerText
                };
            });
        }''')
        
        await browser.close()
        return data
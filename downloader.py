from playwright.sync_api import sync_playwright

class Downloader:

    @staticmethod
    def download(url: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Načtení stránky
            page.goto(url)  # Nahraď URL požadovanou stránkou

            # Získání vykresleného HTML
            html = page.content()

            browser.close()
        return html
    
    @staticmethod
    def save(url: str) -> None:
        html = Downloader.download(url)
        with open("recipe.html", "w", encoding="utf-8") as f:
            f.write(html)
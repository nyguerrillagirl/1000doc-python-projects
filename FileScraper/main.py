from FileScraper import FileScraper


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    xpathStr = '//div[@class="table-responsive"]//table//tbody//tr'
    targetAnchorTag = './td[1]//a'
    file_scraper = FileScraper("sample_page.html", xpathStr, targetAnchorTag, "downloaded_files")
    # file_scraper = FileScraper("https://mirrors.apple2.org.za/ftp.apple.asimov.net/images/magazines/uptime/", xpathStr, targetAnchorTag, "downloaded_files")
    file_scraper.listFilesToDownload()


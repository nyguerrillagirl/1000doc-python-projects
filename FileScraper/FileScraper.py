from scrapy import Selector
import requests
from urllib.parse import urljoin
import time

class FileScraper:

    def __init__(self, urlOrFilePath, xmlPathStr1, anchorXPath, targetFolderPath, fileFormat ="*.*", downloadDelay = 10):
        '''
        Initializes key variables for the FileScraper class.

        :param urlPath: The website page we will examine for files to download
        :param xmlPathStr1: The xmlpath that will search for to extract file links from the website page
        :param anchorXPath: The xpath to target the anchor tag that contains the file link
        :param targetFolderPath: The folder path where the downloaded files will be saved
        :param fileFormat: The file format to filter the downloaded files by (default is "*.*" which means all file formats)
        :param downloadDelay: The delay in seconds between each file download to prevent overwhelming the server (default is 10 seconds)
        '''
        self.urlOrFilePath = urlOrFilePath
        if urlOrFilePath.startswith('http://') or urlOrFilePath.startswith('https://'):
            print("Reading in HTML content from URL...")
            self.isUrl = True
            self.html_contents = self._readInHtmlFromURL(urlOrFilePath)
        else:
            print("Reading in file content from file path...")
            self.isUrl = False
            self.html_contents = self._readInFile(self.urlOrFilePath, 'r')

        self.xmlPathStr1 = xmlPathStr1
        self.xmlPathTarget = anchorXPath
        self.targetFolderPath = targetFolderPath
        self._createFolder(self.targetFolderPath)
        self.fileFormat = fileFormat
        self.downloadDelay = downloadDelay

    def _createFolder(self, folderPath):
        '''
        This method will create a folder at the specified folder path if it does not already exist.

        :param folderPath: The path of the folder to be created
        '''
        import os
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
            print(f"Created folder: {folderPath}")
        else:
            print(f"Folder already exists: {folderPath}")

    def _readInHtmlFromURL(self, url):
        '''
        This method will read in the HTML content from the specified URL and return it as a string.

        :param url: The URL of the website page to read
        :return: The HTML content of the website page as a string
        '''
        response = requests.get(url)
        htmlContent = response.text
        return htmlContent

    def _readInFile(self, filePath, mode):
        '''
        This method will read in a file from the specified file path and return its contents as a string.

        :param filePath: The path to the file that needs to be read
        :param mode: The mode in which to open the file (e.g., 'r' for read, 'w' for write)
        :return: The contents of the file as a string
        '''
        with open(filePath, mode) as file:
            content = file.read()
        return content

    def listFilesToDownload(self):
        '''
        This method will list all the files that match the specified file format from the website page.
        It will use the xmlPathStr to extract file links and print them out.
        '''
        sel = Selector(text=self.html_contents)
        # get to the location to start looking for href
        rows = sel.xpath(self.xmlPathStr1)

        for row in rows:
            time.sleep(self.downloadDelay)
            # find the anchor tag that contains the file link using the target anchor xpath
            link = row.xpath(self.xmlPathTarget)

            href = link.xpath('./@href').get()
            filename = link.xpath('normalize-space(text())').get()
            print(f"Found file: {filename} with link: {href}")


    def startDownloading(self):
        sel = Selector(text=self.html_contents)

        rows = sel.xpath(self.xmlPathStr1)

        for row in rows:
            link = row.xpath(self.xmlPathTarget)

            href = link.xpath('./@href').get()
            filename = link.xpath('normalize-space(text())').get()
            print(f"Found file: {filename} with link: {href}")

            file_url = urljoin(self.urlOrFilePath, href) if self.isUrl else href

            # download the file
            response = requests.get(file_url)
            # save the file locally
            with open(f"{self.targetFolderPath}/{filename}", 'wb') as file:
                file.write(response.content)

            break  # only do one to test, remove this break statement to download all files

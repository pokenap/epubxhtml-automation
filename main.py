"""This is an epub xhtml file generator made by parsing text with identifiers and regex to create individual pages for chapters and images.
The program's variables can be modified through the config.toml in the main directory.
"""

import argparse
import os
import re
import requests
import tempfile
import sys
import toml
import Templates.templates as epub
import Helper.TextEditing as TextEditing
            
def main():
    #Initialization
    #Arguments
    parser = argparse.ArgumentParser(
                        prog="EPUB_XHTML_Generator",
                        description="Creates xhtml files for epub use"
    )

    parser.add_argument('--url', help='path of source')
    parser.add_argument('--path', help='path of source text')
    parser.add_argument('--title', help='book title')
    parser.add_argument('--dlimages', action='store_true' , help='automatically download images')

    args = parser.parse_args()

    with open('config.toml', 'r') as configFile:
        config = toml.load(configFile)

    #Globals
    #Path to text file containing novel text.
    pathOriginal = args.path if args.path else config['source']['file_path']

    #Title to be added into xhtml header
    title = args.title if args.title else config['info']['title']

    #Page url
    urlRoot = args.url[:26] if args.url else config['source']['url_root']
    urlPath = args.url[26:] if args.url else config['source']['url_path']
    fullUrl = urlRoot + urlPath

    #Regex patterns
    patterns = config['regex']['patterns']

    #Html identifiers
    identifiers = config['html']['identifiers']
    htmlImage = config['html']['image']
    htmlStart = config['html']['start']
    htmlEnd = config['html']['end']
    startIdx = config['html']['start_idx']
    endIdx = config['html']['end_idx']

    #Flags
    useStartEndIndices = config['html']['use_idx']
    chapterOnDifPage = config['xhtml']['chapter_on_dif_page']
    downloadImages = args.dlimages if args.dlimages else config['download']['download_images']
    
    #Starting index for xhtml files (Number of last premade file)
    fileNameFolder = config['create']['folder']
    fileNameIndex = config['create']['index_offset']
    fileNameTemplate = config['create']['name']
    fileType = '.xhtml'

    #File path of file being written to
    currentFilePath = './' + fileNameFolder + '/' + fileNameTemplate + f'{fileNameIndex:04}' + fileType

    #Source download location
    sourceMainFolder = config['download']['source']
    sourceFolder = config['download']['source_sub']
    sourcePath = sourceMainFolder + '/' + sourceFolder

    
    #Image download location
    imageMainFolder = config['download']['images']
    imageFolder = config['download']['images_sub']
    imagePath = imageMainFolder + '/' + imageFolder

    #Sanity checks
    if not fullUrl and not pathOriginal:
        print('Program needs at least either a url or path to source file.')
        sys.exit()

    #Create directories if they do not exist
    try:
        os.mkdir(sourceMainFolder)
    except:
        print('Main source directory already exists')

    try:
        os.mkdir(sourcePath)
    except:
        print('Source directory already exists')

    try:
        os.mkdir(imageMainFolder)
    except :
        print('Main image directory already exists')

    try:
        os.mkdir(imagePath)
    except :
        print('Image directory already exists')    

    try:
        os.mkdir('./' + fileNameFolder)
    except:
        print('Output directory already exists') 


    #Source download
    headers = config['download']['user_agent'] 
    sourceName = config['download']['source_name']
    sourceFullPath = sourcePath + '/' + sourceName

    if pathOriginal is None:
        with open(sourceFullPath, 'wb') as file:
            response = requests.get(fullUrl, headers=headers)
            file.write(response.content)
        pathOriginal = sourceFullPath

    #Updated during runtime
    linesList = []
    afterImage = False
    
    #Helper Methods
    def filePathUpdate():
        """Sets the current file path to the most recently created file."""
        nonlocal currentFilePath
        nonlocal fileNameIndex
        fileNameIndex += 1
        currentFilePath = './' + fileNameFolder + '/' + fileNameTemplate + f'{fileNameIndex:04}' + fileType

    def newFile():
        """Creates a new file after writing any lines left in the queue to the working file."""
        writeCurrentQueue()
        filePathUpdate()
        with open(currentFilePath, 'x'):
            pass
    
    def writeCurrentQueue():
        """Writes the current lines in the queue to the working file."""
        nonlocal linesList
        nonlocal afterImage
        if linesList:
            with open(currentFilePath, 'a', encoding='utf-8') as output:
                if afterImage:
                    text = epub.xhtmlStart(title) + epub.xhtmlBody(linesList) + epub.xhtmlEnd()
                    output.write(text)
                else:
                    text = epub.xhtmlBody(linesList) + epub.xhtmlEnd()
                    output.write(text)
            linesList.clear()
        if afterImage:
            afterImage = False

    def downloadImage(url:str):
        """Downloads an image from a given url.
        Currently, hardcoded to search two levels of html for the image url.
        """
        imageUrl = ''
        with tempfile.TemporaryFile(delete_on_close=False) as temp:
                response = requests.get(url, headers=headers)
                temp.write(response.content)
                temp.close()

        with open(temp.name, mode='r', encoding='utf-8') as html:
            for line in html:
                if line.find('class=\"fullImageLink\"') != -1:
                    text = TextEditing.imageUrlFinder(line, line.find('class=\"fullImageLink\"'))
                    imageUrl = urlRoot + text
                    break

        imageName = '/' + TextEditing.nameFromUrl(url)

        with open(imagePath + imageName, 'wb') as file:
            response = requests.get(imageUrl, headers=headers)
            file.write(response.content)

    def handleSamePageHeader(line):
        """Generates a page with a header without closing the html allowing more text to be written."""
        nonlocal afterImage
        newFile()
        with open(currentFilePath, 'a', encoding='utf-8') as output:
            heading = TextEditing.htmlElementRemover(line)
            text = epub.xhtmlStart(title) + epub.xhtmlPageHeading(heading)
            output.write(text)
        if afterImage:
            afterImage = False

    def handleSeparatePageHeader(line):
        """Generates a page with a header and closes the html."""
        nonlocal afterImage
        newFile()
        with open(currentFilePath, 'a', encoding='utf-8') as output:
            names = TextEditing.chapterNameParser(TextEditing.htmlElementRemover(line), separators=[':', '–'])
            text = epub.xhtmlChapterPage(names[0], names[1:], title)
            output.write(text)
        if afterImage:
            afterImage = False

    def handleNoHeaderPage():
        """Generates a page with no header without closing the html allowing more text to be written."""
        nonlocal afterImage
        newFile()
        with open(currentFilePath, 'a', encoding='utf-8') as output:
            text = epub.xhtmlStart(title)
            output.write(text)
        if afterImage:
            afterImage = False

    def handleImagePage(line):
        """Generates a page with an image and closes the html."""
        nonlocal afterImage
        if fullUrl and downloadImages:
            imageUrl = urlRoot + TextEditing.imageUrlFinder(line)
            downloadImage(imageUrl)
        newFile()
        with open(currentFilePath, 'a', encoding='utf-8') as output:
            text = epub.xhtmlImage(TextEditing.nameFromUrl(TextEditing.imageUrlFinder(line)))
            output.write(text)
        newFile()
        if not afterImage:
            afterImage = True
        

    #Main text parse loop
    with open(pathOriginal, 'r', encoding='utf-8') as source:
        startingLine = 0
        #Use config index or make a single pass up to the provided start identifier.
        if not useStartEndIndices:
            for idx, line in enumerate(source):
                if line.find(htmlStart) != -1 or line is None:
                    startingLine = idx 
                    break
        else:
            startingLine = startIdx

        #Reset file pointer
        source.seek(0)

        #Parse file line by line
        for idx, line in enumerate(source):
            if idx < startingLine:
                continue
            if useStartEndIndices:
                if idx > endIdx:
                    break
            if any(line.find(i) != -1 for i in identifiers):
                if chapterOnDifPage:
                    handleSeparatePageHeader(line)
                    handleNoHeaderPage()
                else:
                    handleSamePageHeader(line)
            elif re.search(patterns[0], line):
                if chapterOnDifPage:
                    handleSeparatePageHeader(line)
                else:
                    handleSamePageHeader(line)
            elif any(re.search(i, line) for i in patterns[1:]):
                handleSamePageHeader(line)
            elif line.find(htmlImage) != -1:
                handleImagePage(line)
            elif line.find(htmlEnd) != -1:
                writeCurrentQueue()
                break
            else:
                linesList.append(line)
            

if __name__ == "__main__":
    main()


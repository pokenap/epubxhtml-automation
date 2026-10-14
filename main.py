import argparse
import os
import re
import requests
import sys
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

    args = parser.parse_args()

    if args.path is None and args.url is None:
        print('Provide either a url or a text path')
        sys.exit()
    elif args.path and args.url:
        print('Provide only one of a url or a text path')
        sys.exit()

    #Globals
    #Path to text file containing novel text.
    pathOriginal = args.path

    #Title to be added into xhtml header
    title = args.title

    #Starting index for xhtml files (Number of last premade file)
    fileNameFolder = './xhtml/'
    fileNameIndex = 6
    fileNameTemplate = 'Section'
    fileType = '.xhtml'

    

    #File path of file being written to
    currentFilePath = fileNameFolder + fileNameTemplate + f'{fileNameIndex:04}' + fileType

    #Source download location
    sourceMainFolder = './Source'
    sourceFolder = '/GT 1'
    sourcePath = sourceMainFolder + sourceFolder

    try:
        os.mkdir(sourceMainFolder)
    except:
        print('Main source directory already exists')

    try:
        os.mkdir(sourcePath)
    except:
        print('Source directory already exists')

    #Image download location
    imageMainFolder = './Images'
    imageFolder = '/GT 1'
    imagePath = imageMainFolder + imageFolder

    try:
        os.mkdir(imageMainFolder)
    except :
        print('Main image directory already exists')

    try:
        os.mkdir(imagePath)
    except :
        print('Image directory already exists')    

    #Source download
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36'}

    if pathOriginal is None:
        url = args.url
        with open(sourcePath + '/source.html', 'wb') as file:
            response = requests.get(url, headers=headers)
            file.write(response.content)
        pathOriginal = sourcePath + '/source.html'
    

    linesList = []
    
    #Helper Methods
    def filePathUpdate():
        nonlocal currentFilePath
        nonlocal fileNameIndex
        fileNameIndex += 1
        currentFilePath = fileNameFolder + fileNameTemplate + f'{fileNameIndex:04}' + fileType

    def newFile():
        writeCurrentQueue()
        filePathUpdate()
        with open(currentFilePath, 'x'):
            pass
    
    def writeCurrentQueue():
        nonlocal linesList
        if linesList:
            with open(currentFilePath, 'a', encoding='utf-8') as output:
                text = epub.xhtmlBody(linesList)
                output.write(text)
            linesList.clear()

    def downloadImage(url:str):
        imageName = '/' + TextEditing.nameFromUrl(url)
        print(imageName)
        with open(imagePath + imageName, 'wb') as file:
            response = requests.get(url, headers=headers)
            file.write(response.content)


    partRegex = r"Part\s[0-9]"
    chapterRegex = r'Chapter\s[0-9]'
    betweentheLinexRegex = r'Between\sthe\sLines\s'

    #Main text parse loop
    with open(pathOriginal, 'r', encoding='utf-8') as source:
        enumerated = enumerate(source)

        for idx, line in enumerated:
            if line.find('<p><br>') >= 0 or line is None:
                startingLine = idx + 2
                break
    
        for idx, line in enumerated:
            if idx < startingLine:
                continue
            if re.search(chapterRegex, line):
                newFile()
                with open(currentFilePath, 'a', encoding='utf-8') as output:
                    names = TextEditing.chapterNameParser(TextEditing.htmlElementRemover(line), separators=[':', '—'])
                    text = epub.xhtmlChapterPage(names[0], names[1:], title)
                    output.write(text)
            elif line.find('id=\"Prologue') != -1 or line.find('id=\"Epilogue') != -1 or line.find('id=\"Afterword') != -1 or line.find('id=\"Ending\"') != -1:
                newFile()
                with open(currentFilePath, 'a', encoding='utf-8') as output:
                    names = TextEditing.chapterNameParser(TextEditing.htmlElementRemover(line), separators=[':', '—'])
                    text = epub.xhtmlChapterPage(names[0], names[1:], title)
                    output.write(text)
                newFile()
                with open(currentFilePath, 'a', encoding='utf-8') as output:
                    text = epub.xhtmlStart(title)
                    output.write(text)              
            elif re.search(partRegex, line) or re.search(betweentheLinexRegex, line):
                newFile()
                with open(currentFilePath, 'a', encoding='utf-8') as output:
                    heading = TextEditing.htmlElementRemover(line)
                    text = epub.xhtmlPageHeading(heading, title)
                    output.write(text)
            elif line.find('<table') != -1:
                writeCurrentQueue()
                break
            elif line.find('<figure') != -1:
                url = args.url[:25] + TextEditing.imageUrlFinder(line)
                downloadImage(url)
                newFile()
                with open(currentFilePath, 'a', encoding='utf-8') as output:
                    text = epub.xhtmlImage(TextEditing.nameFromUrl(url))
                    output.write(text)
            else:
                linesList.append(line)





        

if __name__ == "__main__":
    main()


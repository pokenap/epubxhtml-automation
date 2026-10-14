import argparse
import re
import Templates.templates as epub
import Helper.TextEditing as TextEditing
            
def main():
    #Initialization
    #Arguments
    parser = argparse.ArgumentParser(
                        prog="EPUB_XHTML_Generator",
                        description="Creates xhtml files for epub use"
    )

    parser.add_argument('path', help='path of source text')
    parser.add_argument('--title', help='book title')

    args = parser.parse_args()

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
        print(startingLine)
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
            else:
                linesList.append(line)





        

if __name__ == "__main__":
    main()


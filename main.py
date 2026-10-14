import argparse
import re
import Templates.templates as epub

def htmlElementRemover(line:str):
    readingText = False
    lastChar = ''
    output = ''
    for char in line:
        if (lastChar == '>' and char != '<'):
            readingText = True
        
        if readingText and char == '<':
            readingText = False
            break
        
        if readingText:
            output = output + char

        lastChar = char

    return output

def chapterNameParser(line:str, separators:list[str]=[':']):
    names = []
    currentName = ''
    separatorIdx = 0

    for char in line:
        if separatorIdx < len(separators):
            if char == separators[separatorIdx]:
                names.append(currentName)
                currentName = ''
                separatorIdx += 1
            else:
                currentName = currentName + char 
        else:
            currentName = currentName + char 
    names.append(currentName)          

    return names
        


            
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

    #Path to text file containing novel text.
    pathOriginal = args.path

    #Title to be added into xhtml header
    title = args.title
    
    #Starting index for xhtml files (Number of last premade file)
    fileNameStartingIndex = 6
    fileNameIndex = fileNameStartingIndex
    fileNameTemplate = 'Section'
    fileType = '.xhtml'
    currentFilePath = './xhtml/' + fileNameTemplate + f'{fileNameIndex:04}' + fileType

    partRegex = r"{Part}\s[0-9]"
    chapterRegex = r'{Chapter}\s[0-9]'
    betweentheLinexRegex = r'{Between\sthe\sLines\s}[0-9]'

    with open(currentFilePath, 'x'):
        pass

    #Main text parse loop
    with open(pathOriginal, 'r', encoding='utf-8') as source:
        for line in source:
            if line.find('Prologue') != -1 or line.find('Epilogue') != -1 or line.find('Afterword') != -1  or re.search(chapterRegex, line):
                with open(currentFilePath, 'a') as output:
                    names = chapterNameParser(htmlElementRemover(line), separators=[':', '–'])
                    text = epub.xhtmlChapterPage(names[0], names[1:], title)
                    output.write(text)
            else:
                pass




        

if __name__ == "__main__":
    main()


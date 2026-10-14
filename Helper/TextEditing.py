"""TextEditing is a module that handles text parsing.
Examples of such would be extracting text from html elements.
"""
def htmlElementRemover(line:str):
    readingText = False
    lastChar = ''
    output = ''
    for char in line:
        if lastChar == '>' and char != '<':
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

def imageUrlFinder(line:str):
    startingIdx = line.find('href=')
    readingUrl = False
    lastChar = ''
    output = ''
    for idx, char in enumerate(line):
        if idx < startingIdx:
            continue

        if lastChar == '\"' and char != '\"':
            readingUrl = True

        if readingUrl and char == '\"':
            readingUrl = False
            break

        if readingUrl:
            output = output + char

        lastChar = char

    return output 

def nameFromUrl(line:str):
    startingIdx = line.find('File:') + len('File:')
    output = ''
    for idx, char in enumerate(line):
        if idx < startingIdx:
            continue
        output = output + char

    return output 
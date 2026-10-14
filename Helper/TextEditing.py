"""TextEditing is a module that handles text parsing.
Examples of such would be extracting text from html elements.
"""
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
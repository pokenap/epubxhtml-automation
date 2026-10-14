import requests
import tempfile

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

def download(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36'}
    with open('source.html', 'wb') as file:
        response = requests.get(url, headers=headers)
        file.write(response.content)
        print(response.ok)

def imageUrlFinder(line:str, start:int=0):
    startingIdx = line.find('href=', start)
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

def downloadImage(url:str):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36'}
    mainUrl = url[:26]
    imageUrl = ''
    with tempfile.TemporaryFile(delete_on_close=False) as temp:
        response = requests.get(url, headers=headers)
        temp.write(response.content)
        temp.close()

        with open(temp.name, mode='r', encoding='utf-8') as html:
            for line in html:
                if line.find('class=\"fullImageLink\"') != -1:
                    text = imageUrlFinder(line, line.find('class=\"fullImageLink\"'))
                    imageUrl = mainUrl + text
                    break
    
    print(imageUrl)
    imageName = '/' + nameFromUrl(url)
    
    with open('./Images/GT 1' + imageName, 'wb') as file:
        response = requests.get(imageUrl, headers=headers)
        file.write(response.content)

def openFile(path):
    with open(path, 'r', encoding='utf-8') as source:
        enumerated = enumerate(source)
        for idx, line in enumerated:
            print(idx)


#print(htmlElementRemover(text))


#print(nameFromUrl(imageUrlFinder(text)))


openFile('./Source/GT 1/source.html')


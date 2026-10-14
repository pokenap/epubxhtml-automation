import requests
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

def download():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36'}
    url = 'https://www.baka-tsuki.org/project/index.php?title=Toaru_Majutsu_no_Index:GT_Volume1'
    with open('source.html', 'wb') as file:
        response = requests.get(url, headers=headers)
        file.write(response.content)
        print(response.ok)

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

def downloadImage(url:str):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36'}
    imageName = nameFromUrl(url)
    with open(imageName, 'wb') as file:
        response = requests.get(url, headers=headers)
        file.write(response.content)

text = '''<figure class="mw-default-size" typeof="mw:File/Thumb"><a href="/project/index.php?title=File:GT_Index_v01_032.jpg" class="mw-file-description"><img src="/project/thu
'''

#print(htmlElementRemover(text))


#print(nameFromUrl(imageUrlFinder(text)))

downloadImage('https://www.baka-tsuki.org/project/index.php?title=File:GT_Index_v01_032.jpg')


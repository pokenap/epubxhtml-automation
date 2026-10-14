import re

partRegex = r"^Part\s[0-9]"
chapterRegex = r'^Chapter\s[0-9]'

#Path to text file containing novel text.
pathOriginal = r'./text.txt'

#Title to be added into xhtml header
title = "A Certain Magical Index: Genesis Testament - Volume 9"

htmlImage = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
    <title>{title}</title>
    
  <link href="stylesheet.css" rel="stylesheet" type="text/css"/>
<link href="page_styles.css" rel="stylesheet" type="text/css"/>
</head>
  <body class="calibre">
  <h2 class="block_9" id="toc_id_3"></h2>
	<p class="block_"><img src="../Images/" alt="Image" class="calibre1"/></p>
</body>
</html>'''

linesArray = []

#Starting index for xhtml files (Number of last premade file)
fileNameStartingIndex = 6
fileNameIndex = fileNameStartingIndex
fileNameTemplate = 'Section'
fileType = '.xhtml'
currentFilePath = ''

def writeToFile():
    if len(linesArray) > 0:
        with open(currentFilePath, 'a', encoding='utf-8') as f:
            for line in linesArray:
                f.write(line + '\n')

def startOfFile():
    global fileNameIndex
    global currentFilePath
    writeToFile()
    linesArray.clear()
    fileNameIndex += 1
    newFilePath = './xhtml/' + fileNameTemplate + f'{fileNameIndex:04}' + fileType
    currentFilePath = newFilePath
    with open(newFilePath, 'w', encoding='utf-8') as nf:
        pass

#Opens text file from path variable, cases cover different chapters, parts, and images
#Images need manual keyword added beforehand
with open(pathOriginal, encoding='utf-8') as f:
    for line in f:
        if line.find('ImageHere') >= 0:
            startOfFile()
            with open(currentFilePath, 'w', encoding='utf-8') as nf:
                nf.write(htmlImage)
            startOfFile()
        elif line.find('Between the Lines') >= 0:
            startOfFile()
            htmlStart = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
    <title>{title}</title>
    
  <link href="../Styles/stylesheet.css" rel="stylesheet" type="text/css"/>
<link href="../Styles/page_styles.css" rel="stylesheet" type="text/css"/>
</head>
  <body class="calibre">
<p class="block_4">
<span class="text_1">
</span></p>
	<h2 class="block_9" id="toc_id_2">{line}</h2>\n
'''
            linesArray.append(htmlStart)
        elif re.search(partRegex, line):
            startOfFile()
            htmlStart = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
    <title>{title}</title>
    
  <link href="../Styles/stylesheet.css" rel="stylesheet" type="text/css"/>
<link href="../Styles/page_styles.css" rel="stylesheet" type="text/css"/>
</head>
  <body class="calibre">
<p class="block_4">
<span class="text_1">
</span></p>
	<h2 class="block_9" id="toc_id_10">{line.replace('Part ', '')}</h2>\n
'''
            linesArray.append(htmlStart)
        elif re.search(chapterRegex, line):
            startOfFile()
            chapterHtml = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
    <title>{title}</title>
    
  <link href="../Styles/stylesheet.css" rel="stylesheet" type="text/css"/>
<link href="../Styles/page_styles.css" rel="stylesheet" type="text/css"/>
</head>
  <body class="calibre">
<h1 class="block_10" id="toc_id_1">{line}</h1>
	<p class="block_3"></p>
	<p class="block_4"><span class="text_"></span><span class="text_1"><br class="calibre7" id="calibre_pb_13"/>
</span></p>
</body>
</html>
'''
            with open(currentFilePath, 'w', encoding='utf-8') as nf:
                nf.write(chapterHtml)
        else:
            prefix = r'<p class="block_5">'
            suffix = r'</p>'
            line.replace('\n', '')
            linesArray.append(prefix + line + suffix)  
    writeToFile()        

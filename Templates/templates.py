"""Templates is a module that contains frequently recurring xhtml strings to be used and manipulated with the contained functions.
Examples of such would be xhtml headers and xhtml image links.
"""

type Lines = list[str]

def xhtmlStart(title=""):
    """Generates the xhtml header.
    Takes an optional title of book as an argument.
    """
    return f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
    <title>{title}</title>
    
    <link href="../Styles/stylesheet.css" rel="stylesheet" type="text/css"/>
    <link href="../Styles/page_styles.css" rel="stylesheet" type="text/css"/>
</head>
<body class="calibre">
'''

def xhtmlEnd(footer=""):
    """Generates the xhtml footer and closing html tag.
    Takes an optional footer.
    """
    return f'''
{footer}
</body>
</html>
'''

def xhtmlChapterPage(chapterName:str, chapterSubNames:list[str], title="", toc:int=1):
    """Generates an individual page for the chapter title, number, etc.
    Takes the main chapter name.
    Takes chapter sub headings, names, etc.
    Takes an optional title of book as an argument.
    Takes an optional Table of Contents id number.
    """

    chapterText = f'<h1 class="block_10" id="toc_id_{toc}">{chapterName}</h1>\n'

    if chapterSubNames:
        for idx, subname in enumerate(chapterSubNames):
            if idx % 2:
                chapterText = chapterText + f'<p class="block_4"><span class="text_">{subname}</span></p>\n'
            else:
                chapterText = chapterText + f'<p class="block_3">{subname}</p>\n'

    return xhtmlStart(title) + chapterText + xhtmlEnd()

def xhtmlPageHeading(heading:str, title="", toc:int=2):
    """Generates a heading for a page. Used for chapter title on same page as text
    Takes the heading text.
    Takes an optional title of book as an argument.
    Takes an optional Table of Contents id number.
    """

    processed = heading

    if heading.find('Part ') != -1:
        processed = heading.replace('Part ', '')
    headingText = f'<h2 class="block_9" id="toc_id_{toc}">{processed}</h2>\n'

    return xhtmlStart(title) + headingText

def xhtmlBody(bodyArr:Lines):
    """Generates xhtml body text using an array of strings."""
    output = ""

    prefix = r'<p class="block_5">'
    suffix = r'</p>'

    for line in bodyArr:
        output = output + prefix + line + suffix

    return output

def xhtmlImage(name:str,title=""):
    imageText = f'''<h2 class="block_9" id="toc_id_3"></h2>
        <p class="block_"><img src="../Images/{name}" alt="Image" class="calibre1"/></p>
        '''
    
    return xhtmlStart(title) + imageText + xhtmlEnd()
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

text = '''<h2><span id="Prologue:_At_an_Early_Christmas_Eve_Intersection_.E2.80.93_Prepare_for_Xmas_Eve.21"></span><span class="mw-headline" id="Prologue:_At_an_Early_Christmas_Eve_Intersection_–_Prepare_for_Xmas_Eve!">Prologue: At an Early Christmas Eve Intersection – Prepare_for_Xmas_Eve!</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="https://www.baka-tsuki.org/project/index.php?title=Toaru_Majutsu_no_Index:GT_Volume1_Prologue&amp;action=edit&amp;section=T-1" title="Edit section: Prologue: At an Early Christmas Eve Intersection – Prepare_for_Xmas_Eve!"><span>edit</span></a><span class="mw-editsection-bracket">]</span></span></h2>
'''

print(htmlElementRemover(text))

if text.find('open'):
    print('open')
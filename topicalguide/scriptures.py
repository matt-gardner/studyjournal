#!/usr/bin/env python

books = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua',
        'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings',
        '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job',
        'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah',
        'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel',
        'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah',
        'Haggai', 'Zechariah', 'Malachi', 'Matthew', 'Mark', 'Luke', 'John',
        'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians',
        'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians',
        '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon',
        'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John',
        'Jude', 'Revelation', '1 Nephi', '2 Nephi', 'Jacob', 'Enos', 'Jarom',
        'Omni', 'Words of Mormon', 'Mosiah', 'Alma', 'Helaman', '3 Nephi',
        '4 Nephi', 'Mormon', 'Ether', 'Moroni', 'D&C',
        'Doctrine and Covenants', 'Moses', 'Abraham']

links = ['gen','ex','lev','num','duet','josh','judg','ruth','1_sam','2_sam',
        '1_kgs','2_kgs','1_chr','2_chr','ezra','neh','esth','job','ps','prov',
        'eccl','song','isa','jer','lam','ezek','dan','hosea','joel','amos',
        'obad','jonah','micah','nahum','hab','zeph','hag','zech','mal','matt',
        'mark','luke','john','acts','rom','1_cor','2_cor','gal','eph','philip',
        'col','1_thes','2_thes','1_tim','2_tim','titus','philem','heb','james',
        '1_pet','2_pet','1_jn','2_jn','3_jn','judge','rev','1_ne','2_ne',
        'jacob','enos','jarom','omni','w_of_m','mosiah','alma','hel','3_ne',
        '4_ne','morm','ether','moro','dc','dc','moses','abr']

def clean_reference(ref):
    ref= ref.replace(',', '')
    if '(' in ref:
        substring = ref[ref.find('('):ref.find(')')+1]
        ref = ref.replace(substring,'')
    return ref

def split_for_sorting(reference):
    reference = clean_reference(reference)
    items = reference.split()
    for i, item in enumerate(items):
        if ':' in item or (item.isdigit() and i != 0):
            ref_book = ' '.join(items[:i])
            chverse = item.split(':')
            chapter = int(chverse[0])
            verse = ''
            if len(chverse) > 1:
                j = 0
                while j < len(chverse[1]) and chverse[1][j].isdigit():
                    j += 1
                verse = int(chverse[1][:j])
            rest = ' '.join(items[i:])
            break
    else:
        return (len(books)+2, 'unknown', 'unknown', 'unknown')
    for i, book in enumerate(books):
        if ref_book == book:
            return (i, chapter, verse, rest)
    return (i+1, chapter, verse, rest)


def get_link(reference):
    return get_link_part(reference, '', '')


def get_link_part(reference, book, chapter):
    link = ''
    after_link = ''
    items = reference.split()
    i = 0
    if book and chapter:
        if ',' in reference:
            verse = reference[:reference.find(',')+1]
        else:
            verse = reference
    if not book:
        book = items[i]
        i, comma = advance_i(i, items)
        while book not in books:
            if i >= len(items):
                return reference
            book += ' ' + items[i]
            i, comma = advance_i(i, items)
    if not chapter:
        if ':' in items[i]:
            try:
                chapter, verse = items[i].split(':')
            except ValueError:
                chverse = items[i].split(':')
                chapter = chverse[0]
                verse = chverse[1]
                if '-' in verse:
                    verse = verse.split('-')[0]
        else:
            chapter = items[i]
            verse = ''
    i, comma = advance_i(i, items)
    if comma or ',' in chapter:
        chapter = chapter.replace(',','')
        reference = ' '.join(items[:i])+' '
        ref = ' '.join(items[i:])
        if items[i][0].isdigit():
            after_link = get_link_part(ref, book, '')
        else:
            after_link = get_link_part(ref, '', '')
    verserange = verse
    if '-' in verse:
        verse = verse.split('-')[0]
    if ',' in verserange:
        verserange = verserange.replace(',','')
        reference = ' '.join(items[:i])+' '
        verse = verse.replace(',','')
        ref = ' '.join(items[i:])
        if items[i][0].isdigit():
            if ':' in items[i]:
                after_link += get_link_part(ref, book, '')
            else:
                n = 0
                while i+n < len(items) and items[i+n][0].isdigit():
                    if ':' in items[i+n]:
                        reference = ' '.join(items[:i+n])+' '
                        after_link += get_link_part(' '.join(items[i+n:]), book, '')
                        break
                    verserange += ','+items[i+n].replace(',','')
                    n += 1
                else:
                    reference = reference + ref
        else:
            after_link += get_link_part(ref, '', '')
    link += make_link(reference, book, chapter, verserange, verse)
    link += after_link
    return link

def advance_i(i, items):
    i += 1
    comma = False
    if i < len(items) and '(' in items[i]:
        while ')' not in items[i]:
            i += 1
        if ',' in items[i]:
            comma = True
        i += 1
    return i, comma

def make_link(ref, book, chapter, verserange, verse):
    for i, b in enumerate(books):
        if book == b:
            link = '<a href="http://scriptures.lds.org/en/'+links[i]+'/'+str(chapter)
            if verserange:
                link += '/'+verserange+'#'+verse
            link += '">'+ref+'</a>'
            return link
    return ref


def get_book(reference):
    reference = clean_reference(reference)
    items = reference.split()
    i = 0
    book = items[i]
    i += 1
    while book not in books:
        if i >= len(items):
            return 'Bad'
        book += ' ' + items[i]
        i += 1
    return book

        

# vim: et sw=4 sts=4

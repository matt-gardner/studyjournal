#!/usr/bin/env python

books = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua',
        'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings',
        '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job',
        'Psalms', 'Proverbs', 'Ecclesiastes', 'The Song of Solomon', 'Isaiah',
        'Jeremiah', 'Lamentations', 'Ezekial', 'Daniel', 'Hosea', 'Joel',
        'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah',
        'Haggai', 'Zechariah', 'Malachi', 'Matthew', 'Mark', 'Luke', 'John',
        'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians',
        'Ephesians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
        '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James',
        '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude',
        'Revelation', '1 Nephi', '2 Nephi', 'Jacob', 'Enos', 'Jarom', 'Omni',
        'Words of Mormon', 'Mosiah', 'Alma', 'Helaman', '3 Nephi', '4 Nephi',
        'Mormon', 'Ether', 'Moroni', 'D&C', 'Doctrine and Covenants', 'Moses',
        'Abraham']

def split_for_sorting(reference):
    # We get rid of commas to make it easier to find where the book is.
    # It's ok 'cause we're just sorting by book.  We treat them better when
    # figuring out where to split links up.
    reference = reference.replace(',', '')
    items = reference.split()
    for i, item in enumerate(items):
        if ':' in item or (item.isdigit() and i != 0):
            ref_book = ' '.join(items[:i])
            chapter = int(item.split(':')[0])
            rest = ' '.join(items[i:])
            break
    else:
        return (len(books)+2, 'unknown', 'unknown')
    for i, book in enumerate(books):
        if ref_book == book:
            return (i, chapter, rest)
    return (i+1, chapter, rest)


# vim: et sw=4 sts=4

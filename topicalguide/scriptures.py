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
    items = reference.split()
    if ':' in items[1]:
        ref_book = items[0]
        rest = items[1:]
    elif ':' in items[2]:
        ref_book = ' '.join(items[:2])
        rest = items[2:]
    for i, book in enumerate(books):
        if ref_book == book:
            return (i, rest)
    return (i+1, rest)


# vim: et sw=4 sts=4

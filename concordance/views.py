from django.shortcuts import render
import os
import json
import re
from django.core.paginator import Paginator
# import nltk
# from nltk.corpus import wordnet
# from nltk.stem import WordNetLemmatizer, SnowballStemmer

# i ran these by saving them here (not as comments, obviously) and running this file 
# nltk.download('wordnet')  # this had to be run one time after pip install nltk
# nltk.download('punkt') # this had to be run one time after pip install nltk


# ABOUT PAGE 
def about(request):
    # I had to rewrite the file to have books as keys and to have the digits of the chapters and verses in each entry

    # script_dir = os.path.dirname(__file__)
    # file_path = os.path.join(script_dir, 'KJV-old-backup2.json')

    # with open(file_path, 'r') as file:
    #     data = json.load(file)

    # books = {}
    # for entry in data:
    #     name_match = re.match(r'^([\w\s]+)\s(\d+:\d+)', entry['name'])
    #     if name_match:
    #         book_name = name_match.group(1)
    #         chapter_and_verse_numbers = name_match.group(2)

    #         if book_name not in books:
    #             books[book_name] = []

    #         entry['chapter_and_verse'] = chapter_and_verse_numbers
    #         books[book_name].append(entry)

    # with open(file_path, 'w') as file:
    #     json.dump(books, file, indent=4)

    return render(request, 'about.html')


# SEARCH FUNCTION / HOME PAGE
def search(request):
    if request.GET.get("term"):

        term = request.GET.get("term")
        book = request.GET.get("book")

        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'KJV.json')

        total_occurrences = 0
        results = []
        verse_occurrences = 0

        with open(file_path, 'r') as f:
            data = json.load(f)

            if not request.GET.get("case_specific"):
                regex = re.compile(r"(?<!\w){}(?!\w)".format(term), re.IGNORECASE)
                # regex = re.compile(r"\b{}\b".format(re.escape(term)), re.IGNORECASE)

                case_specific = False

            elif request.GET.get("case_specific"):
                regex = re.compile(r"(?<!\w){}(?!\w)".format(term))
                # regex = re.compile(r"\b{}\b".format(term))
                case_specific = True
            if book:
                if book in data:
                    book_entries = data[book]
                    for entry in book_entries:
                        # if entry["name"].startswith(book):
                        matches = regex.findall(entry[u'verse'])
                        if matches:
                        # verse_occurrences.add(entry[u'name'])
                            verse_occurrences += 1
                            for match in matches:
                                total_occurrences += 1
                                # Modify the matched term to include bold tags
                                modified_match = "<b>{}</b>".format(match)
                                # Replace the matched term in the verse with the modified version
                                entry[u'verse'] = entry[u'verse'].replace(match, modified_match)
                            results.append((f"<span class='chapter-verse'>{entry[u'name']}</span>", entry[u'verse']))
            else:
                for book_entries in data.values():
                    for entry in book_entries:
                        matches = regex.findall(entry['verse'])
                        if matches:
                            verse_occurrences += 1
                            for match in matches:
                                total_occurrences += 1
                                # Modify the matched term to include bold tags
                                modified_match = "<b>{}</b>".format(match)
                                # Replace the matched term in the verse with the modified version
                                entry[u'verse'] = entry[u'verse'].replace(match, modified_match)
                            results.append((f"<span class='chapter-verse'>{entry[u'name']}</span>", entry[u'verse']))

        # PAGINATION ANCHOR 
            if book:
                pagination_anchor = f"/concordance/search?book={book}&term={term}" 
            elif not book:
                pagination_anchor = f"/concordance/search?term={term}"
            if request.GET.get("case_specific"):
                pagination_anchor = pagination_anchor + "&case_specific=on"

            pagination_anchor = pagination_anchor + "&page="

            paginator = Paginator(results, 12)
            page = request.GET.get('page', 1)
            pagination = paginator.get_page(page)
            page = int(page)

            context = {
                "results": pagination,
                "term": term,
                "total_verse_occurrences": verse_occurrences,
                "total_occurrences": total_occurrences,
                "case_specific": case_specific,
                "book": book,
                "pagination_anchor": pagination_anchor,
                "next": page + 1 if pagination.has_next() else None,
                "prev": page - 1  if pagination.has_previous() else None,
                "elided_page_numbers": paginator.get_elided_page_range(page, on_each_side=4, on_ends=1)
            }
    else:
        context = {'actual_match': None}

    return render(request, 'home.html', context)

# LIST OF BOOKS
def by_book(request):
    base_url = "/concordance"
    appended = "/read?book=" if request.GET.get("read") else "/search?book="
    # chapter_number = "&chapter=1"
    url = base_url + appended
    OLD_TESTAMENT_URLs = {
        "Genesis": url, "Exodus": url, "Leviticus": url, "Numbers": url, "Deuteronomy": url, "Joshua": url, "Judges": url,
        "Ruth": url, "First Samuel": url, "Second Samuel": url, "First Kings": url, "Second Kings": url, "First Chronicles": url, "Second Chronicles": url,
        "Ezra": url, "Nehemiah": url, "Esther": url, "Job": url, "Psalms": url, "Proverbs": url, "Ecclesiastes": url,
        "Song of Solomon": url, "Isaiah": url, "Jeremiah": url, "Lamentations": url, "Ezekiel": url, "Daniel": url, "Hosea": url,
        "Joel": url, "Amos": url, "Obadiah": url, "Jonah": url, "Micah": url, "Nahum": url, "Habakkuk": url,
        "Zephaniah": url, "Haggai": url, "Zechariah": url, "Malachi": url,
    }
    NEW_TESTAMENT_URLs = {
        "Matthew": url, "Mark": url, "Luke": url, "John": url, "Acts": url, "Romans": url, "First Corinthians": url,
        "Second Corinthians": url, "Galatians": url, "Ephesians": url, "Philippians": url, "Colossians": url, "First Thessalonians": url, "Second Thessalonians": url,
        "First Timothy": url, "Second Timothy": url, "Titus": url, "Philemon": url, "Hebrews": url, "James": url, "First Peter": url,
        "Second Peter": url, "First John": url, "Second John": url, "Third John": url, "Jude": url, "Revelation": url
    }

    context = {
        "OLD_TESTAMENT": OLD_TESTAMENT_URLs,
        "NEW_TESTAMENT": NEW_TESTAMENT_URLs,
        # "chapter_number": chapter_number
    }
    return render(request, 'books.html', context)

#  READ CHAPTER 
def read(request):
    BIBLE_CHAPTERS = {
        "Genesis": 50, "Exodus": 40, "Leviticus": 27, "Numbers": 36, "Deuteronomy": 34, "Joshua": 24, "Judges": 21, "Ruth": 4, "First Samuel": 31,
        "Second Samuel": 24, "First Kings": 22, "Second Kings": 25, "First Chronicles": 29, "Second Chronicles": 36, "Ezra": 10, "Nehemiah": 13, "Esther": 10, "Job": 42, 
        "Psalms": 150, "Proverbs": 31, "Ecclesiastes": 12, "Song of Solomon": 8, "Isaiah": 66, "Jeremiah": 52, "Lamentations": 5, "Ezekiel": 48, "Daniel": 12,
        "Hosea": 14, "Joel": 3, "Amos": 9, "Obadiah": 1, "Jonah": 4, "Micah": 7, "Nahum": 3, "Habakkuk": 3, "Zephaniah": 3,
        "Haggai": 2, "Zechariah": 14, "Malachi": 4,
        
        "Matthew": 28, "Mark": 16, "Luke": 24, "John": 21, "Acts": 28, "Romans": 16, "First Corinthians": 16, "Second Corinthians": 13, "Galatians": 6,
        "Ephesians": 6, "Philippians": 4, "Colossians": 4, "First Thessalonians": 5, "Second Thessalonians": 3, "First Timothy": 6, "Second Timothy": 4, "Titus": 3, "Philemon": 1,
        "Hebrews": 13, "James": 5, "First Peter": 5, "Second Peter": 3, "First John": 5, "Second John": 1, "Third John": 1, "Jude": 1, "Revelation": 22
    }

    try:
        book = request.GET["book"]
        chapter = request.GET["chapter"]
        if not chapter.isdigit():
            chapter = 1
    except KeyError:
        return render(request, "error.html", status=400)
    else:
        results = [] 
        chapter = int(chapter)

        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'KJV.json')

        with open(file_path, 'r') as f:
            data = json.load(f)

            try:
                print (book, "the books")
                book_entries = data[book]
            except KeyError:
                print("derp")
                return render(request, "error.html", status=400)
            else:
                for entry in book_entries:
                    # chapter_number = int(entry['name'].split(':')[0].split(' ')[-1])
                    chapter_number = int(entry['chapter_and_verse'].split(':')[0])
                    if chapter_number == chapter:
                        results.append((f"<span class='chapter-verse'>{entry[u'chapter_and_verse']}</span>", entry[u'verse']))

                number_of_chapters = BIBLE_CHAPTERS.get(book)

                elided_pagination = create_paginated_list(chapter, number_of_chapters, 9)

                context = {
                    "number_of_chapters": number_of_chapters,
                    "read_chapter": results,
                    "book":book,
                    "chapter": chapter,
                    "elided_pagination": elided_pagination,
                    "current_chapter": chapter,
                }
        return render(request, 'books.html', context)

# PAGINATOR 
def create_paginated_list(chapter_number, total_number, allowed_per_page):
    result = []
    first_page = False
    last_page = False

    if total_number > allowed_per_page:
        if chapter_number <= 5:
            result = list(range(1, 10)) + ["..."]
        elif chapter_number >= total_number - 4:
            result = ["..."] + list(range(total_number - 8, total_number + 1))
        else:
            result = ["..."] + list(range(chapter_number - 4, chapter_number + 1)) + list(range(chapter_number + 1, chapter_number + 5)) + ["..."]
    else:
        result = list(range(1, total_number + 1))

    if chapter_number == 1:
        first_page = True
    elif chapter_number == total_number:
        last_page = True

    return {"numbers": result, "first_page":first_page, "last_page":last_page}

# OLD WAY 

                # if book:
                #     for entry in data:
                        
                #         if entry["name"].startswith(book):
                #             chapter_number = int(entry['name'].split(':')[0].split(' ')[-1])
                #             current_chapter = chapter
                #             if chapter_number == chapter:
                #                 results.append((f"<span class='chapter-verse'>{entry[u'name']}</span>", entry[u'verse']))
                
                # else:
                
                #     for entry in data:
                #         matches = regex.findall(entry['verse'])
                #         if matches:
                #             verse_occurrences += 1
                #             for match in matches:
                #                 total_occurrences += 1
                #                 # Modify the matched term to include bold tags
                #                 modified_match = "<b>{}</b>".format(match)
                #                 # Replace the matched term in the verse with the modified version
                #                 entry[u'verse'] = entry[u'verse'].replace(match, modified_match)
                #             results.append((f"<span class='chapter-verse'>{entry[u'name']}</span>", entry[u'verse']))

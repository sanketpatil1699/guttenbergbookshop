from django.shortcuts import render
from .models import Author,Book,BookbookLanguage,Bookshelves,BookbookSubject,Booksbookshelf,BookFormat,BooksLanguage,BooksSubject
from django.http import HttpResponse
import sys
from rest_framework.decorators import action

@action(methods=["Post"], detail=False)
def getBooksData(request):
    """
    Author : Sanket Patil.
    Date : 17-03-2024
    The function `getBooksData` retrieves and processes data related to books and authors based on user
    input, and handles exceptions if any occur.
    
    :param request: The given code snippet is a Python function that retrieves data related to books
    based on a selected subject name from a dropdown menu in a web application. Here's a breakdown of
    the code:
    :return: The `getBooksData` function is returning a rendered HTML template named 'dash.html' with
    the context data containing the list of subjects (`subjData`) and the sorted list of book details
    (`sortingDownloadCount`).
    """
    try:
        global subjData, allDetails,sortingDownloadCount
        subjData = []
        allDetails = []
        sortingDownloadCount=[]
        selected_name = request.POST.get('selected_name') #selected_name getting which one is selected from dropdown.
        
        # Bewlow functionality is for colleting all data from various table. 
        if selected_name != '' and selected_name != None:
            idSubject  = BooksSubject.objects.filter(name = selected_name).first()
            BookId = BookbookSubject.objects.filter(subject_id = idSubject.id).values_list('book_id', flat=True)
            
            if BookId:
                authDetails = Author.objects.filter(id__in=BookId)
                books = Book.objects.filter(id__in=BookId)
                url_objects = BookFormat.objects.filter(book_id__in=BookId)
                for bookTitle, author, dwnldUrl,booksId in zip(books, authDetails, url_objects,BookId):
                    booksLanguageID = BookbookLanguage.objects.filter(book_id=booksId).values_list('language_id', flat=True)
                    booksLanguage = BooksLanguage.objects.filter(id__in=booksLanguageID).values_list('code', flat=True)
                    
                    details = {
                            'name': author.name,
                            'birth_year': author.birth_year,
                            'death_year': author.death_year,
                            'download_count': bookTitle.download_count,
                            'title': bookTitle.title,
                            'downloadUR':dwnldUrl.url,
                            'subject': selected_name,
                            'language':booksLanguage[0]
                        }
                    allDetails.append(details)
                sortingDownloadCount = sorted(allDetails, key=lambda x: x['download_count'], reverse=True)
        
        #DropdownList 
        bookSub = BooksSubject.objects.all()[0:200]
        for SubjectData in bookSub:
            subInfo ={
                'name': SubjectData.name,
            } 
            subjData.append(subInfo)
        return  render(request,'dash.html',{'name':subjData,'authDetails':sortingDownloadCount})
    except Exception as e:
        print("----- Error in Change flag -------")
        print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))
        print(e)

        
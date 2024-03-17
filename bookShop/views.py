from django.shortcuts import render
from .models import Author,Book,BookbookLanguage,Bookshelves,BookbookSubject,Booksbookshelf,BookFormat,BooksLanguage,BooksSubject
from django.http import HttpResponse
import sys
from rest_framework.decorators import action

subjData = []
allDetails = []
a=0
b=20
@action(methods=["Post"], detail=False)
def getBooksData(request):
    try:
    # subjData = []
    # allDetails = []
        global subjData, allDetails  # Assuming you want to keep the data persistent across requests
        subjData = []
        allDetails = []
        sortingDownloadCount=[]
        selected_name = request.POST.get('selected_name')
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
        bookSub = BooksSubject.objects.all()[0:20]
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

        
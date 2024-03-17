
from django.db import models

class Author(models.Model):
    id = models.IntegerField(primary_key=True)
    birth_year = models.SmallIntegerField(null=True)
    death_year = models.SmallIntegerField(null=True)
    name = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'books_author'
        
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    download_count = models.IntegerField(blank=True, null=True)
    gutenberg_id = models.IntegerField(unique=True)
    media_type = models.CharField(max_length=16)
    title = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'books_book'
        
class Bookshelves(models.Model):
    id = models.AutoField(primary_key=True)
    book_id = models.IntegerField()
    bookshelf_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'books_book_bookshelves'

class BookbookLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    book_id = models.IntegerField()
    language_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'books_book_languages'

class BookbookSubject(models.Model):
    id = models.AutoField(primary_key=True)
    book_id = models.IntegerField()
    subject_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'books_book_subjects'
        
class Booksbookshelf(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, null=False)

    class Meta:
        managed = False
        db_table = 'books_bookshelf'
        
class BookFormat(models.Model):
    id = models.AutoField(primary_key=True)
    mime_type = models.CharField(max_length=32, null=False)
    url = models.CharField(max_length=256, null=False)
    book_id = models.IntegerField(null=False)

    class Meta:
        managed = False
        db_table = 'books_format'
        
class BooksLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=4, null=False)

    class Meta:
        managed = False  # To inform Django not to manage this table
        db_table = 'books_language'  # Specify the name of the table
        

class BooksSubject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, null=False)

    class Meta:
        managed = False 
        db_table = 'books_subject'
from django.db.models import Count,Min,Max 
from enum import auto
from django.http.response import FileResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render
from .models import Article,Book,ConferenceArticle, GeneralArticle
from django.contrib.auth.decorators import login_required
from .import forms
from django.contrib import messages
from django.shortcuts import get_object_or_404

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter
import datetime
import csv
import xlwt #for excel export

# import for pdf export--------------------
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from io import BytesIO


from django.template.loader import get_template
from django.urls import reverse

from xhtml2pdf import pisa


#pdf export here-------------------------
def create_pdf(request,export_Format):
    articles=Article.objects.filter(author=request.user)
    books =Book.objects.filter(author=request.user)
    conferences =ConferenceArticle.objects.filter(author=request.user)
    print(conferences)

    template_path = 'pdf_template.html'


    context = {'articles': articles, 'books':books,
    'conferences':conferences,'format':export_Format}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="result.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
#export ends-------------------------

#export as excel -------------------------------------
def create_excelSheet(request):
    '''fields from models are exported in the form of column in
    excel format'''
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="result.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('result')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Title', 'authors', 'Journal','Date','volume', 'pages','ArticleLink','Journal Type','SJR rating','Impact Factor','Peer Reviewed','DOI' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    # font_style.num_format_str = 'dd/mm/yyyy'
    # style2 =xlwt.XFStyle()
    # style2.num_format_str ='dd/mm/yyyy'

    journals = Article.objects.filter(author =request.user).values_list('title', 'co_authors','journal','pub_date__year', 'volume', 'pages','article_link','journal_type','sjrRating','impactFactor','peer_reviewed','DOI')
    print("the journals are-------------")
    print(journals)

    
    for row in journals:
        row_num += 1
        for col_num in range(len(row)):
            if col_num ==5: 
                #date column
                ws.write(row_num, col_num, row[col_num], font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)


    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    row_num+=3 # gap of three rows


    columns = ['Title', 'Authors', 'ConferenceName ', 'Date','Volume','Pages','Link','Publisher','DOI' ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    conferences =ConferenceArticle.objects.filter(author=request.user).values_list('title','co_authors','conference_name','pub_date__year','volume','pages','conference_link','publisher','DOI')
    for row in conferences:
        row_num += 1
        for col_num in range(len(row)):
            
            ws.write(row_num, col_num, row[col_num], font_style)
           
    wb.save(response)
    return response
    # return HttpResponse("this will be excel sheet export")

def create_BibtexSheet(request):
    articles = Article.objects.filter(author= request.user)
    print('bibtex from create bibtex')
    bib_entries = []
    conferences =ConferenceArticle.objects.filter(author =request.user)
    books =Book.objects.filter(author=request.user)
    #export works fine for now but the missing fields and the default
    #fields are yet to be worked on

    for article in articles:
        bib_item ={
            'title':article.title,
            'author':article.co_authors,
            'journal':article.journal,
            'pages':article.pages,
            'year':str(article.pub_date.year),
            'ID':str(article.journal_ID),
            'ENTRYTYPE': 'article'

        }
        if article.volume!=0:
            bib_item['volume'] =str(article.volume)
        if article.pages !='':
            bib_item['pages'] =article.pages
        if article.publisher !='':
            bib_item['publisher'] =article.publisher

        bib_entries.append(bib_item.copy())
    
    for conference in conferences:
        bib_item={
            
            'title':conference.title,
            'author':conference.co_authors,
            'book_title':conference.conference_name,
            'year':str(conference.pub_date.year),
            'ID':conference.conference_ID,
            'ENTRYTYPE': 'inproceedings'

        }
        if conference.volume!=0:
            bib_item['volume'] =str(conference.volume)
        if conference.pages !='':
            bib_item['pages'] =conference.pages
        
        bib_entries.append(bib_item.copy())
    
    for book in books:
        bib_item={
            
            'title':book.title,
            'author':book.co_authors,
            'pages':book.pages,
            'year':str(book.pub_date.year),
            'ID':book.book_ID,
            'ENTRYTYPE': 'book'

        }
        if book.pages !='':
            bib_item['pages'] =book.pages
        bib_entries.append(bib_item.copy())

    db = BibDatabase()
    db.entries = bib_entries
    # [
    #     {'journal': 'Nice Journal',
    #     'comments': 'A comment',
    #     'pages': '12--23',
    #     'title': 'An amazing title',
    #     'year': '2013',
    #     'volume': '12',
    #     'ID': 'Cesar2013',
    #     'author': 'Jean Casar',
    #     'ENTRYTYPE': 'article'}
        
    # ]

    # writer = BibTexWriter()
    # writer.write(db)
    # content = writer
    bibtex_str = bibtexparser.dumps(db)
    return HttpResponse(bibtex_str, content_type='text/plain')
    
    
    


def article_list(request):
    if request.user.is_authenticated:
       distincts = Article.objects.filter(author = request.user).values('title').annotate(slug = Max('slug'))
       articles = Article.objects.filter(slug__in = [item['slug'] for item in distincts])

       distincts = Book.objects.filter(author = request.user).values('title').annotate(slug = Max('slug'))
       books = Book.objects.filter(slug__in = [item['slug'] for item in distincts])


       distincts = ConferenceArticle.objects.filter(author=request.user).values('title').annotate(slug = Max('slug'))
       conference_articles = ConferenceArticle.objects.filter(slug__in = [item['slug'] for item in distincts])

       distincts = GeneralArticle.objects.filter(author = request.user).values('title').annotate(slug = Max('slug'))
       general_articles = GeneralArticle.objects.filter(slug__in = [item['slug'] for item in distincts])

    else:
        return HttpResponseRedirect(reverse("accounts:signup"))
    return render(request, 'articleslist.html', {'articles': articles,
    'books':books,'conference_article':conference_articles,'general_articles':general_articles,
    })




#def article_list(request):
#    if request.user.is_authenticated:
#       articles = Article.objects.filter(author=request.user).order_by('pub_date')
#       books = Book.objects.filter(author =request.user)
#       conference_articles=ConferenceArticle.objects.filter(author=request.user)
#      general_articles =GeneralArticle.objects.filter(author=request.user)
#    else:
#        return HttpResponseRedirect(reverse("accounts:signup"))
#    return render(request, 'articleslist.html', {'articles': articles,
#    'books':books,'conference_article':conference_articles,'general_articles':general_articles,
#    })


@login_required(login_url='accounts:login')
def article_create(request, type):
    '''
        all form types are handled here
        form identified according to type parameter of url
        type= journal: it specifies the journal form is requested

    '''
    
    biptexForm = forms.BiptexForm()
    print("type is :"+type)
    if type == 'journal':
        print("yes it is journal")
        form = forms.CreateArticle()

    elif type == 'conference':
        form = forms.CreateConference()

    elif type == 'Book':
        form = forms.CreateBook()
    elif type =='general':
        form= forms.GeneralArticle()

    if request.method == 'POST':
        print(type)
        print("Post request")
        if type == 'journal':
            print("yes it is journal")
            form = forms.CreateArticle(request.POST)

        elif type == 'conference':
            form = forms.CreateConference(request.POST)
        elif type == 'Book':
            form = forms.CreateBook(request.POST)
        elif type == 'general':
            form = forms.GeneralArticle(request.POST)

        # form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('article:list')

    return render(request, 'article_create.html', {'form': form,
                                                   "biptex": biptexForm,
                                                   'type':type})


def article_detail(request, slug):
    # return HttpResponse(slug)
   # form = forms.CreateArticle()
    
    if  Article.objects.filter(slug=slug).exists():
        temp = Article.objects.get(slug=slug)
        type ='article'
        articles =Article.objects.filter(title = temp.title).order_by('version')
    elif Book.objects.filter(slug=slug).exists():
        temp = Book.objects.get(slug = slug)
        type ='book'
        articles=Book.objects.filter(title = temp.title).order_by('version')

    elif ConferenceArticle.objects.filter(slug=slug).exists():
        temp = ConferenceArticle.objects.get(slug = slug)
        type ='conference'
        articles=ConferenceArticle.objects.filter(title=temp.title).order_by('version')
    
    elif GeneralArticle.objects.filter(slug=slug).exists():
        temp = GeneralArticle.objects.get(slug = slug)
        type ='general'
        articles=GeneralArticle.objects.filter(title=temp.title).order_by('version')

    
    return render(request, 'article_obj.html', {'articles': articles,'type':type})


def readbibtex(f):
    bib_database = bibtexparser.load(f)
    print('bib database entries-------------')
    print(bib_database.entries)
    print('------------------------------------')
    return bib_database.entries  # returns dict


def bibtexPopulator(request):
    '''receives multiple bibtex files as input and parse them and 
       create a model for each bibtex to store in database   '''
    biptexForm = forms.BiptexForm()
    if request.method == 'POST':
           
            
        biptexForm = forms.BiptexForm(request.POST, request.FILES)
        files = request.FILES.getlist('bibtex_form') 
        #id of input_file box  is bibtex_form
        # print(files)

        print("got biptex")
        if biptexForm.is_valid():
            for file in files:
                # print(file)
                result = readbibtex(file)
                count =len(result)
                if count>0:
                    for item in result:
                        
                        # print(item)
                        if item.get("ENTRYTYPE")=='article':
                            print("article obtained")
                            pubDate=datetime.date(int(item.get('year','1111')),1,1)
                            new_journal =Article.objects.create(
                                title =item.get('title'),
                                co_authors=item.get('author'),
                                pub_date=pubDate,
                                author =request.user,
                                journal =item.get('journal',''),
                                volume =item.get('volume',0),
                                pages =item.get('pages',''),
                                publisher =item.get('publisher', ''),
                                journal_ID = item.get("ID",'')
                            )
                            new_journal.save()
                            print('journal saved successfully---')

                            
                        elif item.get("ENTRYTYPE")=='inproceedings':
                            print("proceedings obtained")
                            pubDate=datetime.date(int(item.get('year','1111')),1,1)
                            new_obj =ConferenceArticle.objects.create(
                                title =item.get('title'),
                                co_authors=item.get('author'),
                                pub_date=pubDate,
                                author =request.user,
                                conference_name =item.get('booktitle',''),
                                volume =item.get('volume',0),
                                pages =item.get('pages',''),
                                publisher =item.get('organization', ''),
                                conference_ID =item.get('ID','' )

                            )
                        elif item.get("ENTRYTYPE")=='book':
                            #fields are yet to be populated
                            print("book obtained")
                            pubDate=datetime.date(int(item.get('year','1111')),1,1)
                            new_obj =Book.objects.create(
                                title =item.get('title'),
                                co_authors=item.get('author'),
                                pub_date=pubDate,
                                author =request.user,
                               

                            )
                            # new_obj.save(commit=False)
                            # new_obj.author =request.user
                            new_obj.save()
                            print("object saved successfully")

                        print('--------------------')
        messages.info(request, '%s new models added'%count)
        return HttpResponseRedirect(reverse('article:list'))
            
    return render(request,"bibtexForm.html",{'biptex':biptexForm})



def ProfilePage(request):
    return render(request,"profile.html")
    


def EditArticle(request,type,slug):
    
    print("type:"+type)
    print('slug:'+slug)           
    if type == 'article':
        form_data =Article.objects.get(slug=slug)
        print('form data----------------')
        print(form_data)
        print("yes it is journal")
        form = forms.CreateArticle(instance = form_data)

    elif type == 'conference':
        form_data =ConferenceArticle.objects.get(slug=slug)
        form = forms.CreateConference(instance=form_data)

    elif type == 'book':
        form_data =Book.objects.get(slug=slug)
        form = forms.CreateBook(instance=form_data)
    
    elif type == 'general':
        form_data =GeneralArticle.objects.get(slug=slug)
        form = forms.GeneralArticle(instance=form_data)

    if request.method =="POST":
        messages.info(request, 'Edit successful')
        if type =='article':
            form =forms.CreateArticle(request.POST,instance=form_data)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('article:list'))

        elif type =='conference':
            form =forms.CreateConference(request.POST,instance=form_data)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('article:list'))

        elif type =='book':
            form =forms.CreateBook(request.POST,instance=form_data)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('article:list'))
        elif type =='general':
            form =forms.GeneralArticle(request.POST,instance=form_data)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('article:list'))
        
        print(request.POST)


    
    # print(form)
    return render(request,"edit.html",{"form":form,"type":type,
    'slug':slug})
    
def DeleteArticle(request,type,slug):
    #objection deletion logic here
    if type == 'article':
        items =get_object_or_404(Article,slug =slug)
        items = Article.objects.filter(title = items.title)
        for item in items:
            item.delete()
        messages.info(request, 'one article deleted')
        print('deletion successful')
        return HttpResponseRedirect(reverse('article:list'))

    elif type == 'conference':
        items =get_object_or_404(ConferenceArticle,slug =slug)
        items = ConferenceArticle.objects.filter(title = items.title)
        for item in items:
            item.delete()
        messages.info(request, 'one conference deleted')
        print('deletion successful')
        return HttpResponseRedirect(reverse('article:list'))

    elif type == 'book':
        items =get_object_or_404(Book,slug =slug)
        items = Book.objects.filter(title = items.title)
        for item in items:
            item.delete()
        messages.info(request, 'one book deleted')
        print('deletion successful')
        return HttpResponseRedirect(reverse('article:list'))
    
    elif type == 'general':
        items =get_object_or_404(GeneralArticle,slug =slug)
        items = GeneralArticle.objects.filter(title = items.title)
        for item in items:
            item.delete()
        messages.info(request, 'one general article deleted')
        print('deletion successful')
        return HttpResponseRedirect(reverse('article:list'))



    return HttpResponse("<h1>Invalid item selected</h1>")


def UpdateArticle(request, type , slug):

    if type == 'article':
        form_data =Article.objects.get(slug=slug)
        print('form data----------------')
        print(form_data)
        print("yes it is journal")
        form = forms.CreateArticle({"title":form_data.title,"version":form_data.version+1})

    elif type == 'conference':
        form_data =ConferenceArticle.objects.get(slug=slug)
        form = forms.CreateConference({"title":form_data.title,"version":form_data.version+1})

    elif type == 'book':
        form_data =Book.objects.get(slug=slug)
        form = forms.CreateBook({"title":form_data.title,"version":form_data.version+1})
    
    elif type == 'general':
        form_data =GeneralArticle.objects.get(slug=slug)
        form = forms.GeneralArticle({"title":form_data.title,"version":form_data.version+1})

    if request.method =="POST":
        messages.info(request, 'Update successful')
        if type =='article':
            form =forms.CreateArticle(request.POST)
            if form.is_valid():
                instance = form.save(commit = False)
                instance.author = request.user 
                instance.save()
                return HttpResponseRedirect(reverse('article:list'))

        elif type =='conference':
            form =forms.CreateConference(request.POST)
            if form.is_valid():
                instance = form.save(commit = False)
                instance.author = request.user
                instance.save()
                return HttpResponseRedirect(reverse('article:list'))

        elif type =='book':
            form =forms.CreateBook(request.POST)
            if form.is_valid():
                instance = form.save(commit = False)
                instance.author = request.user
                instance.save()
                return HttpResponseRedirect(reverse('article:list'))
        elif type =='general':
            form =forms.GeneralArticle(request.POST)
            if form.is_valid():
                instance = form.save(commit = False)
                instance.author = request.user
                instance.save()
                return HttpResponseRedirect(reverse('article:list'))
        
        print(request.POST)


    
    # print(form)
    return render(request,"update.html",{"form":form,"type":type,
    'slug':slug})
 


from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms import widgets
from django.forms.models import ModelForm
from .import models
from django.forms import ModelForm, TextInput, EmailInput

data_choices=[('National','National'),
             ('International','International')]


class DateInput(forms.DateInput):
    input_type = 'date'

class CreateArticle(forms.ModelForm):
    
    class Meta:
        model = models.Article
        fields ='__all__'
        exclude =['slug','author','journal_ID']
        widgets={
            "pub_date": DateInput(attrs={
                'class': "form-control",
                'style': 'max-width: 200px;',
                'placeholder': 'title'
               
            }),
            'title': TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'title'
                }),
            'co_authors': TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'authors'
                }),
            'journal': TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'authors'
                }),
            'volume':widgets.NumberInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'authors'
                }),
            'issue':widgets.NumberInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'issue'
                }),

            'pages':widgets.TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'Pages in the form 22-33'
                }),
            'description': widgets.Textarea(attrs={
                'class':'form-control',
                'rows':3
                    }),
            
            'publisher':widgets.TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                }),

            'article_link':widgets.URLInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                }),
            'DOI':widgets.TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                }),
            
            'journal_type':forms.Select(attrs={
                'class':'form-control'}),

            'quartile':forms.Select(attrs={
                'class':'form-control'}),

            'impactFactor':widgets.NumberInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                
                }),

            'sjrRating':widgets.NumberInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                
                }),
            'version':forms.HiddenInput(),
            'peer_reviewed':widgets.CheckboxInput(attrs={
               'style':'padding:5px;',
            })
            
            

            
            
            
            
            
              
        
        }

class CreateBook(forms.ModelForm):
    class Meta:
        model = models.Book
        fields ='__all__'
        exclude =['slug','author','book_ID']
        widgets={
            "pub_date": DateInput(attrs={
                'class': "form-control",
                'style': 'max-width: 200px;',
                'placeholder': 'title'
               
            }),
            'title': TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'title'
                }),
            'version':forms.HiddenInput(),
            'co_authors': TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'authors'
                }),
            
            'volume':widgets.NumberInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'volume'
                }),
            'issue':widgets.NumberInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'issue'
                }),

            'pages':widgets.TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'Pages in the form 22-33'
                }),
            'description': widgets.Textarea(attrs={
                'class':'form-control',
                'rows':3
                    }),
            
            'publisher':widgets.TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                }),

            'book_link':widgets.URLInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                }),
            'DOI':widgets.TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                }),
            
            'edition':widgets.TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                }),
            'isbn':widgets.TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                }),
            'chapters':widgets.TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                }),
            
            

            
        }

class CreateConference(forms.ModelForm):
    class Meta:
        model = models.ConferenceArticle
        fields ='__all__'
        exclude =['slug','author','conference_ID']
        widgets={
            "pub_date": DateInput(attrs={
                'class': "form-control",
                'style': 'max-width: 200px;',
                'placeholder': 'title'
               
            }),

            'title': TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'title'
                }),
            'co_authors': TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'authors'
                }),
            'version':forms.HiddenInput(),           
            'volume':widgets.NumberInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'authors'
                }),
            
            'pages':widgets.TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'Pages in the form 22-33'
                }),
            'description': widgets.Textarea(attrs={
                'class':'form-control',
                'rows':3
                    }),
            
            'publisher':widgets.TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                }),

            'conference_link':widgets.URLInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                }),
            'DOI':widgets.TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                }),
            'conference_name':widgets.TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                }),  
           
            }

class GeneralArticle(forms.ModelForm):
    class Meta:
        model = models.GeneralArticle
        fields ='__all__'
        exclude =['slug','author','general_ID']
        widgets={
            "pub_date": DateInput(attrs={
                'class': "form-control",
                'style': 'max-width: 200px;',
                'placeholder': 'title'
               
            }),
            'title': TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'title'
                }),
            'co_authors': TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'authors'
                }),
             'version':forms.HiddenInput(),
            'volume':widgets.NumberInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'authors'
                }),
            
            'pages':widgets.TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                'placeholder': 'Pages in the form 22-33'
                }),
            'description': widgets.Textarea(attrs={
                'class':'form-control',
                'rows':3
                    }),
            
            'publisher':widgets.TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                }),

            'conference_link':widgets.URLInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                }),
            'DOI':widgets.TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                }),
            'conference_name':widgets.TextInput(attrs={
                'class': "form-control",
                'style': 'min-width: 500px;',
                }),  
           
            }




class BiptexForm(forms.Form):
    bibtex_form = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,
    }))

from django import forms

from .models import Entry, Topic

class TopicForm(forms.ModelForm):
    class Meta: #nested class, don't have to define all details of field because of that
        model = Topic 
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model=Entry
        fields = ['text']
        labels = {'text': ''}

        #define a widget so we can customize the label for the field itself

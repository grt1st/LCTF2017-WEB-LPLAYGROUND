from django import forms

class UrlForm(forms.Form):
    #target = forms.CharField(label="Target Enter:", max_length=100)
    target = forms.CharField(label="Target Enter:", max_length=100)
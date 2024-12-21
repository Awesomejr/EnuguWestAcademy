from django import forms

from library.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file and not file.name.endswith('.pdf'):
            raise forms.ValidationError('Only PDF files are allowed.')
        return file
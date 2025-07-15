from django import forms
from .models import Comment, Post
from taggit.forms import TagField

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm): # Add this new form
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body'] # Specify fields to include in the form


class PostForm(forms.ModelForm):
    tags = TagField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'basic-input',
            'placeholder': 'django,blogging,tips'
        }),
        help_text="Comma-separated tags (no spaces)"
    )

    class Meta:
        model = Post
        fields = ['title', 'body', 'tags', 'status']  # Include status field
        widgets = {
            'title': forms.TextInput(attrs={'class': 'basic-input'}),
            'body': forms.Textarea(attrs={'class': 'basic-input h-40'}),
            'status': forms.HiddenInput(),  # We'll control this via the publish button
        }
from django import forms
from blog.models import Post, Comment

class PostForm(forms.ModelForm):
	class Meta():
		model = Post
		field = {'author','title','text'}  # the fields which we want to edit in forms

		widgets ={
			'title': forms.TextInput(attrs = {'class': 'textinputclass'}),  # class 'textinputclass' is the  class which we have made
			'text' : forms.Textarea(attrs = {'class': 'editable medium-editor-textarea postcontent'}) #except postcontent all other classes are default bootstrap classes
		}


class CommentForm(forms.ModelForm):
	class Meta():
		model = Post
		field = {'author','text'}

		widgets ={
		'author': forms.TextInput(attrs= {'class': 'textinputclass'}),
		'text': forms.Textarea(attrs = {'class': 'editable medium-editor-textarea'})

		}
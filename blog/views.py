from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from blog.models import Post,Comment
from django.urls import reverse_lazy
from blog.forms import PostForm,CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
# Create your views here.

class AboutView(TemplateView):
	template_name = 'about.html'


class PostListView(ListView):
	model = Post

	def get_queryset(ListView):
		return Post.objects.filter(published_date_lte = timezone.now()).orderby('-published_date')
		#it will return the list of the rows of posts whose publs date is less than or equal to the current time and
		# will order them in decreasing order (-)

class PostDetailView(DetailView):
	model =  Post

class CreatePostView(LoginRequiredMixin, CreateView):
	login_url = '/login'
	redirect_field_name = 'blog/post_detail.html'  # these 2 fields need to be filled in order to use LoginRequiredMixin to handle the Login required task

	form_class = PostForm
	model = Post

# updating a post also need login required

class PostUpdateView(LoginRequiredMixin,UpdateView):
	login_url = '/login'
	redirect_field_name = 'blog/post_detail.html'
	form_class = PostForm
	model = Post


class PostDelete(LoginRequiredMixin,DeleteView):
	model = Post
	success_url = reverse_lazy('post_list')  #reverse_lazy will only give the success url (i.e where to get back
												# when the post is deleted) only when the post deletion is completed 


#this view is for the drafts that are only created not published

class DraftListView(LoginRequiredMixin,ListView):
	login_url = '/login'
	redirect_field_name = 'blog/post_detail.html'
	model = Post
	def get_queryset(self):
		return Post.objects.filter(published_date_isnull = true).order_by('created_date')
		# we here made a query which will retrieve and ordered by the created date where published_date is null

######################################################################################
######################################################################################

@login_required  #decorator which requires the view to accessed onnly when logged in
def add_comment_to_post(request,pk): # a pk is send too as we want to add comment only to specific post
	post = get_object_or_404(Post,pk=pk)   # get that POST obj or not found
	if request.method == 'POST':   # someone actually filled int he form or hit enter
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect('post_detail',pk = post.pk)

		else:
			form = CommentForm()
		return render(request,'blog/comment_form.html'{'form':form})

@login_required
def comment_approve(request,pk):
	comment = get_object_or_404(Comment,pk = pk)
	comment.approve()  #see the models.py and check approve method in Comment model
	return redirect('post_detail',pk = comment.post.pk)  # redirecting back to same post detail view where the comment was made


@login_required
def comment_remove(request,pk):
	comment = get_object_or_404(Comment)
	post_pk = comment.post.pk  # need to save as by the time it get deleted it can be saved beforehand
	comment.delete()
	return redirect('post_detail',pk = post_pk) # and used here to redirect

@login_required
def post_publish(request,pk):
	post = get_object_or_404(Post,pk=pk)
	post.publish  #check the publish method in the Post Model
	return redirect ('post_detail',pk=pk) # redirecting to the post detail page once the post is published



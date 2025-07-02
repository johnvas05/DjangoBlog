from django.shortcuts import render, get_object_or_404
from .models import Post, Comment # Ensure Comment is imported
from .forms import EmailPostForm, CommentForm # Ensure CommentForm is imported
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.shortcuts import redirect # Add this import for redirect
from taggit.models import Tag

def post_list(request, tag_slug=None):
    object_list = Post.objects.filter(status=Post.Status.PUBLISHED)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number) # Get the Page object for the requested page
    except PageNotAnInteger:
        # If page_number is not an integer, deliver the first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range (e.g., 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  template_name='blog/post/list.html', # Note the path 'blog/post/list.html'
                  context={'posts': posts,
                           'page_obj': posts,
                           'tag': tag})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
        status=Post.Status.PUBLISHED # <--- CHANGE THIS LINE!
    )
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    # Form for users to comment
    form = CommentForm()  # Initialize an empty form for GET requests

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,  # Pass comments to the template
                   'form': form})  # Pass the comment form to the template


# This view is for handling comment submission (using require_POST for safety)
@require_POST  # This decorator ensures the view only accepts POST requests
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None  # Initialize comment to None
    form = CommentForm(data=request.POST)  # Bind submitted data to the form

    if form.is_valid():
        # Create a Comment object but don't save it yet
        comment = form.save(commit=False)
        # Assign the current post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()

    # Redirect to the post detail page after successful comment
    return redirect(post.get_absolute_url())


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False # Flag to indicate if email was sent successfully

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} ({cd['email']}) recommends you read \"{post.title}\""
            message = f"Read \"{post.title}\" at {post_url}\n\n" \
                      f"{cd['name']}'s comments: {cd['comments']}"

            # Get the sender email from settings, fallback to the one provided in form
            from_email = getattr(settings, 'EMAIL_HOST_USER', cd['email'])

            try:
                send_mail(subject, message, from_email, [cd['to']])
                sent = True
            except Exception as e:
                # Log the error if sending fails (for debugging)
                print(f"Error sending email: {e}")
                sent = False # Ensure sent is False if an error occurs

    else:
        form = EmailPostForm() # Initialize an empty form for GET requests

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
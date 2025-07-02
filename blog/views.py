from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail
from django.conf import settings
def post_list(request):
    object_list = Post.objects.filter(status=Post.Status.PUBLISHED) # Get all published posts

    paginator = Paginator(object_list, 3) # 3 posts per page (you can change this number)
    page_number = request.GET.get('page', 1) # Get the current page number from the URL query parameter 'page'

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
                  context={'posts': posts, 'page_obj': posts}) # Pass the Page object to the template

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
        status=Post.Status.PUBLISHED
    )
    return render(request, template_name='blog/post/detail.html', context={'post': post})

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
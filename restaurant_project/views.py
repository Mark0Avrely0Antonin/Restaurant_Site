from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.core.mail import EmailMessage
from datetime import timedelta

from .forms import *
from .models import *
from .utils import generate_token

from django.contrib.auth.mixins import LoginRequiredMixin


def menu_filter(request):
    filter = Menu_Filter(request.GET, queryset = Menu.objects.all())
    return render(request, 'menu_filter.html', {"filter": filter})


def send_action_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject = email_subject, body = email_body, from_email = settings.EMAIL_FROM_USER,
                         to = [user.email]
                         )
    email.send()


def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = User_Account.objects.get(pk = uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS, f'Ваша почта подтверждена, авторизуйтесь {user.username}!')
        return redirect(reverse("main"))
    return render(request, 'activate-failed.html', {"user": user})


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)

            user.profile_username = user.username
            user.save()

            send_action_email(user, request)
            messages.add_message(request, messages.SUCCESS,
                                 f"Аккаунт создан {user.username}! Вам лишь осталось подтвердить свой email чтобы авторизоваться!")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_email_verified:
                messages.error(request,
                               f'Электронная почта не подтверждена {user.username}, пожалуйста, проверьте свою почту')
                return redirect("login")
            login(request, user)
            return redirect("main")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


## PROFILE ###


class Contacts(TemplateView):
    template_name = 'contacts.html'

    def get_context_data(self, **kwargs):
        context = super(Contacts, self).get_context_data()

        context['comments'] = ContactReview.objects.all().order_by('-time_created')

        return context


class CommentAddReview(View):

    def post(self, request):
        user = request.user

        if request.method == 'POST':
            form = ContactsForm(request.POST)
            if form.is_valid():
                comment = form.save(commit = False)
                comment.user = user
                comment.save()
                return redirect('contacts')
        else:
            form = ContactsForm()


def edit_profile(request, slug):
    instance = Profile.objects.get(profile_username = slug)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES or None, instance = instance)
        if form.is_valid():
            profile = form.save(commit = False)
            profile.save()
            return redirect(instance.get_absolute_url())

    else:
        form = ProfileForm(request.FILES or None, instance = instance)
    return render(request, 'edit_profile.html', {'form': form})


class ProfileView(DetailView):
    model = Profile
    template_name = 'profile_view.html'
    context_object_name = 'profile_item'
    slug_field = 'profile_username'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()

        user_last_login = User_Account.objects.get(profile_username = self.kwargs['slug']).last_login
        user_created = User_Account.objects.get(profile_username = self.kwargs['slug']).time_create
        last_login = user_last_login + timedelta(hours = 3)
        created = user_created + timedelta(hours = 3)

        context['last_login'] = last_login
        context['created'] = created

        return context


class LogoutView(auth_views.LogoutView):
    next_page = 'main'
    redirect_field_name = 'main'


## PROFILE ### 
### MENU ###

class MenuView(ListView):
    model = Menu
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super(MenuView, self).get_context_data()
        context['menu_list'] = Menu.objects.all()
        context['category_menu'] = Category.objects.all()
        return context


class AddReview(View):

    def get_context_data(self, **kwargs):
        context = super(AddReview, self).get_context_data()

        review_item = get_object_or_404(Reviews, id = self.kwargs['pk'])
        review_total_likes = review_item.review_total_likes()
        review_total_unlikes = review_item.review_total_unlikes()

        context['review_total_likes'] = review_total_likes
        context['review_total_unlikes'] = review_total_unlikes

    def post(self, request, pk):
        dish = Menu.objects.get(pk = pk)
        user = request.user

        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit = False)
                review.dish = dish
                review.user = user
                review.save()
                return redirect(dish.get_absolute_url())
        else:
            form = ReviewForm()


def review_likes(request, slug):
    user = request.user

    review = get_object_or_404(Reviews, id = request.POST.get('review_id'))

    if user in review.review_unlikes.all():
        review.review_unlikes.remove(user)

    review.review_likes.add(user)
    return HttpResponseRedirect(reverse('view_dish', args = [slug]))


def review_unlikes(request, slug):
    user = request.user

    review_unlikes = get_object_or_404(Reviews, id = request.POST.get('review_unlikes_id'))

    if user in review_unlikes.review_likes.all():
        review_unlikes.review_likes.remove(user)

    review_unlikes.review_unlikes.add(user)
    return HttpResponseRedirect(reverse('view_dish', args = [slug]))


def get_category_menu(request, category_id):
    menu_list = Menu.objects.filter(category_id = category_id)
    categories = Category.objects.all()
    category = Category.objects.get(pk = category_id)
    context = {
        'menu_list': menu_list,
        'categories': categories,
        'category': category
    }
    return render(request, template_name = 'category_menu.html', context = context)


class View_Menu(DetailView):
    model = Menu
    template_name = 'view_dish.html'
    context_object_name = 'dish_item'
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super(View_Menu, self).get_context_data()

        dish_item = get_object_or_404(Menu, url = self.kwargs['slug'])

        dish_total_likes = dish_item.dish_total_likes()

        context['dish_total_likes'] = dish_total_likes

        return context


@login_required
def dish_likes(request, slug):
    user = request.user

    dish = get_object_or_404(Menu, id = request.POST.get('dish_id'))

    if not user in dish.dish_likes.all():
        dish.dish_likes.add(user)
    else:
        dish.dish_likes.remove(user)

    return HttpResponseRedirect(reverse('view_dish', args = [str(slug)]))


class About_Us(TemplateView):
    template_name = 'about_us.html'


### MENU ####

## REGISTER, LOGIN, LOGOUT

## CONTACTS ###

class Change_Password(auth_views.PasswordChangeView):
    template_name = 'change_password.html'
    success_url = 'main'

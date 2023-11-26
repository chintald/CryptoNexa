from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core import serializers
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from CryptoNexa.views import update_crypto_details
from .apis.coinmarketcap.fetch_data import fetch_data, get_dummy_data, get_dummy_data_2
from .apis.helper_functions import process_crypto_data
from .forms import CustomUserForm
from .models import Cryptocurrency, Quote
from .forms import CustomUserForm, UserProfileForm
from .models import User
from BuySell.models import Transaction


def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserForm()
    return render(request, 'CryptoNexa/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'CryptoNexa/login.html', {'form': form})


def get_updated_crypto_data(request, fetch_live_data):
    switch = request.session.get('switch')
    if switch is None:
        request.session['switch'] = 0
        switch = 0

    if request.session.get('currency') is None:
        request.session['currency'] = "USD"
        session_cur = "USD"
    else:
        session_cur = request.session.get('currency')

    if fetch_live_data:
        fetched_data_from_api_session_cur = fetch_data(session_cur)
    else:
        if int(switch) == 0:
            request.session['switch'] = 1

            fetched_data_from_api_session_cur = get_dummy_data_2(session_cur)
        else:
            request.session['switch'] = 0
            fetched_data_from_api_session_cur = get_dummy_data(session_cur)

    crypto_data = fetched_data_from_api_session_cur.get('data')
    crypto_to_send = update_crypto_details(crypto_data, session_cur)
    crypto_data = process_crypto_data(crypto_to_send, session_cur, many=True)
    print("Updated price returned")
    return JsonResponse(crypto_data, safe=False)


def crypto_detail(request, slug):
    try:
        cryptocurrency = Cryptocurrency.objects.get(slug=slug)
    except Cryptocurrency.DoesNotExist:
        cryptocurrency = None

    if request.session.get('currency') is None:
        request.session['currency'] = "USD"
        session_cur = "USD"
    else:
        session_cur = request.session.get('currency')

    data = process_crypto_data(cryptocurrency, session_cur, many=False)

    context = {
        "cryptocurrency": data,
        "session_cur": session_cur
    }

    return render(request, 'crypto/crypto_detail.html', context=context)


def user_logout(request):
    logout(request)
    return redirect('index')


@login_required
def user_profile(request, id):
    user = User.objects.get(id=id)
    return render(request, 'CryptoNexa/profile.html', {'user': user})


# def user_edit_profile(request, id):
#     user = User.objects.get(id=id)
#     return render(request, 'CryptoNexa/edit_profile.html', {'user': user})


@login_required
def user_edit_profile(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            # Save the form data
            form.save()

            return redirect('index')
        else:
            return HttpResponseBadRequest("Invalid form submission. Please check the form data.")
    else:
        form = UserProfileForm(
            initial={'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
                     'photo_id': user.photo_id})

    return render(request, 'CryptoNexa/edit_profile.html', {'form': form})


def payment_history(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'CryptoNexa/payment_history.html', {
        'transactions': transactions
    })

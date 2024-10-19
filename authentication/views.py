from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from social_django.models import UserSocialAuth
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from google.oauth2 import id_token
from google.auth.transport import requests
from django.http import JsonResponse
from django.views.decorators.http import require_POST


@csrf_exempt
def make_sso_login(request):
    return render(request, 'index.html')


def get_google_token(request):
    user = request.user

    social_users = UserSocialAuth.objects.filter(user=user, provider='google-oauth2')

    if social_users.exists():
        social_user = social_users.latest('pk')
        access_token = social_user.extra_data['access_token']

        print(f'{access_token=}')
        return access_token
    else:
        return None

@login_required
def get_all_emails(request):
    try:
        access_token = get_google_token(request)

        creds = Credentials(token=access_token)
        service = build('gmail', 'v1', credentials=creds)

        result = service.users().messages().list(userId='me').execute()
        messages = result.get('messages', [])

        return JsonResponse({'messages': messages})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_single_email(request, message_id):
    access_token = get_google_token(request)
    creds = Credentials(token=access_token)
    service = build('gmail', 'v1', credentials=creds)

    message = service.users().messages().get(userId='me', id=message_id).execute()

    snippet = message.get('snippet')  # Um pequeno resumo do conteúdo do email
    payload = message.get('payload', {})
    headers = payload.get('headers', [])
    body = None

    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                body = part['body'].get('data')

    return JsonResponse({
        'snippet': snippet,
        'headers': headers,
        'body': body
    })


@csrf_exempt
@require_POST
def login_with_google(request):
    token = request.POST.get('token')
    print("chamou?")
    try:
        # Validação do token
        id_info = id_token.verify_oauth2_token(token, requests.Request(), 'YOUR_GOOGLE_CLIENT_ID')

        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return JsonResponse({'error': 'Token inválido'}, status=400)

        # Extraia informações do usuário
        user_google_id = id_info['sub']
        user_email = id_info['email']

        # Autenticar ou criar o usuário no banco de dados
        # Por exemplo, você pode verificar se o usuário já existe e logá-lo
        user, created = User.objects.get_or_create(username=user_google_id, email=user_email)

        # Autenticar o usuário no Django
        login(request, user)

        return JsonResponse({'message': 'Usuário autenticado com sucesso'})

    except ValueError:
        return JsonResponse({'error': 'Falha na validação do token'}, status=400)

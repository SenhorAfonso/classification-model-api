from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from social_django.models import UserSocialAuth
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from django.shortcuts import render, redirect
from os import system
from django.contrib.auth.decorators import login_required


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
def list_email_messages(request):
    try:
        access_token = get_google_token(request)
        
        creds = Credentials(token=access_token)
        service = build('gmail', 'v1', credentials=creds)

        result = service.users().messages().list(userId='me').execute()
        messages = result.get('messages', [])

        return JsonResponse({'messages': messages})

    except UserSocialAuth.DoesNotExist:
        print('Usuário não existe')
        return JsonResponse({'error': 'Usuário não autenticado com o Google.'}, status=401)

    except Exception as e:
        print('Outro erro')
        return JsonResponse({'error': str(e)}, status=500)
    
def get_email_message(request, message_id):
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

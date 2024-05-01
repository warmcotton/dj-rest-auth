import os
import environ

import requests
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from json.decoder import JSONDecodeError
from rest_framework import status

from auths.models import CustomUser


# Create your views here.

env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    callback_url = 	'...'
    client_class = OAuth2Client


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = env('GOOGLE_CALLBACK_URL')
    client_class = OAuth2Client

def google_login(request):
    scope = 'email'
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    callback_url = os.environ.get('GOOGLE_CALLBACK_URL')
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={callback_url}&scope={scope}")


def google_callback(request):
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    callback_url = os.environ.get('GOOGLE_CALLBACK_URL')
    code = request.GET.get('code')

    # 1. 받은 코드로 구글에 access token 요청
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={callback_url}")

    ### 1-1. json으로 변환 & 에러 부분 파싱
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    ### 1-2. 에러 발생 시 종료
    if error is not None:
        raise JSONDecodeError(error)

    ### 1-3. 성공 시 access_token 가져오기
    access_token = token_req_json.get('access_token')
    id_token = token_req_json.get('id_token')
    #################################################################

    # 2. 가져온 access_token으로 이메일값을 구글에 요청
    email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code

    ### 2-1. 에러 발생 시 400 에러 반환
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

    ### 2-2. 성공 시 이메일 가져오기
    email_req_json = email_req.json()
    email = email_req_json.get('email')

    print(access_token)
    print(id_token)
    return JsonResponse({'access': access_token, 'code':code, 'id_token': id_token, 'email':email})

    #################################################################

    # 3. 전달받은 이메일, access_token, code를 바탕으로 회원가입/로그인
    # try:
    #     # 전달받은 이메일로 등록된 유저가 있는지 탐색
    #     user = CustomUser.objects.get(email=email)
    #
    #     # FK로 연결되어 있는 socialaccount 테이블에서 해당 이메일의 유저가 있는지 확인
    #     social_user = SocialAccount.objects.get(user=user)
    #
    #     # 있는데 구글계정이 아니어도 에러
    #     if social_user.provider != 'google':
    #         return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
    #     print(access_token)
    #     print(id_token)
    #     # 이미 Google로 제대로 가입된 유저 => 로그인 & 해당 우저의 jwt 발급
    #     data = {'access_token': access_token, 'code': code, 'id_token': id_token}
    #     accept = requests.post(f"http://localhost:8000/auths/google/", data=data)
    #     accept_status = accept.status_code
    #
    #     # 뭔가 중간에 문제가 생기면 에러
    #     if accept_status != 200:
    #         return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
    #
    #     accept_json = accept.json()
    #     accept_json.pop('user', None)
    #     return JsonResponse(accept_json)
    #
    # except CustomUser.DoesNotExist:
    #     # 전달받은 이메일로 기존에 가입된 유저가 아예 없으면 => 새로 회원가입 & 해당 유저의 jwt 발급
    #     print(access_token)
    #     print(id_token)
    #     data = {'access_token': access_token, 'code': code, 'id_token': id_token}
    #     accept = requests.post(f"http://localhost:8000/auths/google/", data=data)
    #     accept_status = accept.status_code
    #
    #     # 뭔가 중간에 문제가 생기면 에러
    #     if accept_status != 200:
    #         return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
    #
    #     accept_json = accept.json()
    #     accept_json.pop('user', None)
    #     return JsonResponse(accept_json)
    #
    # except SocialAccount.DoesNotExist:
    #     # User는 있는데 SocialAccount가 없을 때 (=일반회원으로 가입된 이메일일때)
    #     return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
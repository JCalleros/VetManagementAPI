import logging
from typing import Optional
from django.conf import settings
from djoser.social.views import ProviderAuthView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.shortcuts import render
from django.middleware.csrf import get_token

logger = logging.getLogger(__name__)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request:Request, *args, **kwargs) -> Response:
        token_res = super().post(request, *args, **kwargs)
        if token_res.status_code == status.HTTP_200_OK:
            token_res.data["message"] = "Login Successful."
        else:
            token_res.data["message"] = "Login Failed"
            logger.error("Access or refresh token not found in login response data")
        return token_res
    
    
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request:Request, *args, **kwargs) -> Response:
        refresh_res = super().post(request, *args, **kwargs)
        if refresh_res.status_code == status.HTTP_200_OK:
            refresh_res.data["message"] = "Access tokens refreshed successfully"
        else:
            refresh_res.data["message"] = "Access or refresh tokens not found in refresh response data"
            logger.error("Access or refresh token not found in response data")
        return refresh_res


# class CustomProviderAuthView(ProviderAuthView):
#     def post(self, request:Request, *args, **kwargs) -> Response:
#         provider_res = request.COOKIES.get("refresh")
        
#         if provider_res.status_code == status.HTTP_201_CREATED:
#             access_token = provider_res.data.get("access")
#             refresh_token = provider_res.data.get("refresh")

#             if access_token and refresh_token:
#                 set_auth_cookies(
#                     provider_res,
#                     access_token=access_token,
#                     refresh_token=refresh_token,
#                 )

#                 provider_res.data.pop("access", None)
#                 provider_res.data.pop("refresh", None)

#                 provider_res.data["message"] = "You are logged in Successful."
#             else:
#                 provider_res.data["message"] = (
#                     "Access or refresh token not found in provider response"
#                 )
#                 logger.error(
#                     "Access or refresh token not found in provider response data"
#                 )

#         return provider_res


class LogoutAPIView(APIView):
    def post(self, request: Request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        response.delete_cookie("logged_in")
        return response
        
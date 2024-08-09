from django.shortcuts import render
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['GET','POST','PATCH','DELETE'])
def InterviwerViews(request, pk=None):
    
    if request.method=='GET':
        if pk is not None:
            try:
                Interviewerobj=Interviewer.objects.get(pk=pk)
                serializers=interviwerSerializer(Interviewerobj)
                return Response(serializers.data)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            Interviewerobj=Interviewer.objects.all()
            serializers=interviwerSerializer(Interviewerobj,many=True).data
            return Response(serializers)
        
    elif request.method=='POST':
        try:
          interviewer_data=request.data
        except:
            return Response (status=status.HTTP_404_NOT_FOUND)
        serializers=interviwerSerializer(data=interviewer_data)
        if serializers.is_valid():
            serializers.save()
            return Response('Interviwer Added ',status=status.HTTP_200_OK)
        
        return Response(serializers.errors,status=status.HTTP_404_NOT_FOUND)
    elif request.method=='PATCH':
        try:
            interviewer_data=Interviewer.objects.get(pk=pk)
            print(interviewer_data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializers=interviwerSerializer(interviewer_data,data=request.data,partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response('Update Successfully',status=status.HTTP_200_OK)
        return Response(serializers.errors,status=status.HTTP_404_NOT_FOUND)
    
    elif request.method=='DELETE':
        try:
          interviewer_data=Interviewer.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        interviewer_data.delete()
        return Response('Delete Successfull',status=status.HTTP_200_OK)


    


        


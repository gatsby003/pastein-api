
import arrow

import hashlib

from django.core.cache import cache
from django.db.models import F
from django.shortcuts import render
from .models import Paste, PasteAnalytic
from .serializers import PasteAnalyticSerializer, PasteSerializer

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


LIVE_FOREVER = 2 ** 31 - 1

class PasteView(APIView):
    """List a Paste."""
    def get(self, request, key):
        cached = cache.get(key)

        if cached:
            # repeating code refactor !!!
            view_count_key = f'{key}-view-count'
            view_count = cache.get(view_count_key) or 0

            cache.set(view_count_key, view_count + 1, timeout=LIVE_FOREVER)

            return Response(
                status=status.HTTP_200_OK,
                data=cached
            )

        if Paste.objects.filter(key=key).exists():
            paste = Paste.objects.filter(key=key).first()

            serializer = PasteSerializer(paste)

            # should be moved to analytics middleware and redis should store analytics details 
            # periodically moved to db with a background job
            PasteAnalytic.objects.filter(paste=paste).update(
                view_count = F('view_count') + 1
            )

            cache.set(key, serializer.data, timeout= 2 * 60 * 60)

            view_count_key = f'{key}-view-count'
            view_count = cache.get(view_count_key) or 0

            cache.set(view_count_key, view_count + 1, timeout=LIVE_FOREVER)

            return Response(
                status=status.HTTP_200_OK,
                data=serializer.data
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        key = request.data.get('key')
        content = request.data.get('content')

        if not content:
            return Response(
                data={
                    'message' : 'Empty content not allowed.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if key:
            if Paste.objects.filter(key=key).exists():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            date = str(arrow.utcnow())
            unique_str = content + date
            key = hashlib.sha1(unique_str.encode('ascii')).hexdigest()
            key = key[:6]
        
        paste = Paste.objects.create(
            key=key,
            content=content
        )

        PasteAnalytic.objects.create(
            paste=paste
        )

        serializer = PasteSerializer(paste)

        return Response(
                status=status.HTTP_200_OK,
                data=serializer.data
            )

class PasteAnalyticsView(APIView):
    """Show analytics"""
    def get(self, request, key):
        view_count_key = f'{key}-view-count'
        view_count = cache.get(view_count_key) or 0
        if view_count:
            return Response(
                data={
                    'key': key,
                    'view_count': view_count
                }
            )
        else:
            return Response(
               status=status.HTTP_400_BAD_REQUEST,
            )
        


        




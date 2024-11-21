from django.http import JsonResponse
from rest_framework.response import Response
from django.views import View
import json
from django.shortcuts import get_object_or_404
from .models import Entry
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

# @method_decorator(csrf_exempt, name='dispatch')
class CreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        try:
            data = request.data
            name = data.get('name')
            type_value = data.get('type')
            parent_id = data.get('parent_id')
            user = request.user
            if not name or type_value not in ['folder', 'file']:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': "Invalid name or type."})

            parent = get_object_or_404(Entry, id=parent_id, owner=user) if parent_id else None

            if parent and parent.type != 'folder':
                # return JsonResponse({"error": "Files and folders can only exist in folders."}, status=400)
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': "Files and folders can only exist in folders."})

            entry = Entry.objects.create(name=name, type=type_value, parent=parent, owner=user)

            return Response({'status': status.HTTP_200_OK, 'message': "Record created successfully"})
        except Exception as e:
            print(e)
            return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': e})



class RenameView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        try:
            data = request.data
            new_name = data.get('name')
            id = data.get('id')
            user = request.user
            try:
                entry = get_object_or_404(Entry, id=id, owner=user)
            except Exception as e:
                return Response(
            {"status": status.HTTP_404_NOT_FOUND, "message": "Entry not found or you do not have permission to access it."},
            status=status.HTTP_404_NOT_FOUND)
            if not new_name:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': "New name is required."})

            entry.name = new_name
            entry.save()
            # return JsonResponse({"id": entry.id, "name": entry.name, "type": entry.type})
            return Response({'status':status.HTTP_200_OK, 'message': "Record name updated successfully!"})
        except Exception as e:
            print(e)
            return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': e})


class EntryDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        try:
            data = request.data
            id = data.get('id')
            user = request.user
            try:
                entry = get_object_or_404(Entry, id=id, owner=user)
            except Exception as e:
                return Response(
            {"status": status.HTTP_404_NOT_FOUND, "message": "Entry not found or you do not have permission to access it."},
            status=status.HTTP_404_NOT_FOUND)

            if not entry.parent:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': "Root folders cannot be deleted."},status=status.HTTP_400_BAD_REQUEST,)

            entry.delete()  # Django cascades deletion to children
            return Response({'status':status.HTTP_200_OK, 'message': "Deleted successfully!"})
        except Exception as e:
            print(e)
            return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': e},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class EntryMoveView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        try:
            data = request.data
            parent_id = data.get('to_parent_id')
            id = data.get('id')
            user = request.user
            try:
                entry = get_object_or_404(Entry, id=id, owner=user)
            except Exception as e:
                return Response(
            {"status": status.HTTP_404_NOT_FOUND, "message": "Entry not found or you do not have permission to access it."},
            status=status.HTTP_404_NOT_FOUND,)
            new_parent = get_object_or_404(Entry, id=parent_id, owner=user) if parent_id else None

            if new_parent and new_parent.type != 'folder':
                return Response({'status':status.HTTP_400_BAD_REQUEST,"message": "Files and folders can only be moved to folders."}, status=status.HTTP_400_BAD_REQUEST)

            entry.parent = new_parent
            entry.save()
            return Response({'status':status.HTTP_200_OK, 'message': "Record moved successfully!"},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': e},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EntryListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        try:
            contents=[]
            user = request.user
            data=request.GET
            id=data.get("id")
            name = data.get("name")
            if id:
                try:
                    folder = get_object_or_404(Entry, id=id, owner=user)
                except Exception as e:
                    return Response(
                {"status": status.HTTP_404_NOT_FOUND, "message": "Entry not found or you do not have permission to access it."},
                status=status.HTTP_404_NOT_FOUND,)
                if folder.type != 'folder':
                    return Response({'status':status.HTTP_400_BAD_REQUEST,"message": "Only folders can contain entries."}, status=status.HTTP_400_BAD_REQUEST)

                children = folder.children.all()
                if name:
                    children = children.filter(name__icontains=name)

                contents = [{"id": child.id, "name": child.name, "type": child.type} for child in children]
            else:
                folder =Entry.objects.filter(owner=user)
                if name:
                    folder = folder.filter(name__icontains=name)
                if folder:
                    contents = [{"id": child.id, "name": child.name, "type": child.type,"parent_id":child.parent.id if child.parent else ""} for child in folder]
            return Response({'status':status.HTTP_200_OK, 'message': "Record listed successfully!",'data':contents},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EntryListHierarchyView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        try:
            user = request.user
            data = request.GET
            item_id = data.get("id")

            if not item_id:
                return Response(
                    {"status": status.HTTP_400_BAD_REQUEST, "message": "Item ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            item = get_object_or_404(Entry, id=item_id, owner=user)

            folder_list = []
            if item.type == "file":
                folder_list.append({
                    "id": item.id,
                    "name": item.name,
                    "type": item.type,
                    "parent_id": item.parent.id if item.parent else None,
                })
                item = item.parent

            while item is not None:
                folder_list.append({
                    "id": item.id,
                    "name": item.name,
                    "type": item.type,
                    "parent_id": item.parent.id if item.parent else None,
                })
                item = item.parent

            folder_list = folder_list[::-1]

            return Response(
                {"status": status.HTTP_200_OK, "message": " Folder listed successfully!", "data": folder_list},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            print(e)
            return Response(
                {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

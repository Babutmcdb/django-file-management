from django.urls import path
from .views import CreateView, RenameView, EntryDeleteView, EntryMoveView, EntryListView,EntryListHierarchyView

urlpatterns = [
    path('create/', CreateView.as_view(), name='entry_create'),
    path('rename/', RenameView.as_view(), name='entry_rename'),
    path('delete/', EntryDeleteView.as_view(), name='entry_delete'),
    path('move/', EntryMoveView.as_view(), name='entry_move'),
    path('list/', EntryListView.as_view(), name='entry_list'),
    path('list-hierarchy/', EntryListHierarchyView.as_view(), name='entry_list'),
]

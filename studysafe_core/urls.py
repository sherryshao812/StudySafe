from django.urls import path
from .api_views import *


urlpatterns = [
    path('api/record/access/all', all_access_records.as_view(), name = 'all_access_records'),
    path('api/record/create', create_access_record.as_view(), name = 'create_access_record'),

    path('api/venue/visited/<str:uid>', view_visited_venues.as_view(), name = 'view_visited_venues'),
    path('api/venue/create', create_venue.as_view(), name = 'create_venue'),
    path('api/venue/view/<str:venue_code>', view_venue.as_view(), name = 'view_venue'),
    path('api/venue/view-all', view_all_venues.as_view(), name = 'view_all_venues'),
    path('api/venue/modify/<str:venue_code>', modify_venue.as_view(), name = 'modify_venue'),
    path('api/venue/delete/<str:venue_code>', delete_venue.as_view(), name = 'delete_venue'),

    path('api/member/close-contacts/<str:uid>/<str:date>', view_close_contacts.as_view(), name = 'view_close_contacts'),
    path('api/member/create', create_member.as_view(), name = 'create_member'),
    path('api/member/list-all', list_all_members.as_view(), name = 'list_all_members'),
    path('api/member/view/<str:uid>', view_member.as_view(), name = 'view_member'),
    path('api/member/modify/<str:uid>', modify_member.as_view(), name = 'modify_member'),
    path('api/member/delete/<str:uid>', delete_member.as_view(), name = 'delete_member')
]

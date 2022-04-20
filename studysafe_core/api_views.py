from rest_framework import generics
from .serializers import *
from .models import VisitRecord
from .models import HKUMember
from .models import Venue

"""
Author: Anchit Mishra
This class provides the ListAPIView functionality of displaying
all access for all members' entries/exits to/from all venues.
"""
class all_access_records(generics.ListAPIView):
    queryset = VisitRecord.objects.all()
    serializer_class = VisitRecordSerializer

"""
Author: Anchit Mishra
This class provides the CreateAPIView functionality of creating new access records
(via devices which will be implemented later, not part of this project).
Using this, new records of members' entries/exits to/from venues can be created.
"""
class create_access_record(generics.CreateAPIView):
    queryset = VisitRecord.objects.all()
    serializer_class = VisitRecordSerializer

"""
Author: Ajayveer Singh
This class provies the ListAPIView functionality of listing all the venues that
have been visited by a specified HKUMember.
"""
class view_visited_venues(generics.ListAPIView):
    serializer_class = VenueSerializer
    def get_queryset(self, **kwargs):
        uid = self.kwargs['uid']
        visit_records_of_member = VisitRecord.objects.filter(member_uid=uid).values('venue_code')
        return Venue.objects.filter(venue_code__in = visit_records_of_member)

"""
Author: Ajayveer Singh
This class provides the ListAPIView functionality of listing all the close contacts.
"""
class view_close_contacts(generics.ListAPIView):
    serializer_class = HKUMemberSerializer
    def get_queryset(self, **kwargs):

        from datetime import datetime, timedelta

        # UID of infected person and date of first confirmed positive test/onset of symptoms
        uid = self.kwargs['uid']
        date = datetime.strptime(self.kwargs['date'], '%Y-%m-%d')

        # Get the UIDs of all the people who used the same venues on the same days as infected (within 2 day span)
        dates = [(date - timedelta(days=2)).strftime("%Y-%m-%d"), (date - timedelta(days=1)).strftime("%Y-%m-%d"), (date).strftime("%Y-%m-%d")]
        potential_close_contacts = VisitRecord.objects.filter(record_datetime__date__in = dates).values('member_uid').distinct()
        #print(potential_close_contacts)

        # stores UIDs of close contacts
        close_contacts = []

        # Pairs up 2 visit records - the entry and exit record for a student visitng a venue
        entry_exit_pairs = []

        # Process all visit records one member at a time
        for potential_close_contact in potential_close_contacts:

            # NOT GETTING RECORDS NEEDS FIX
            potential_close_contact_uid = potential_close_contact['member_uid']
            visit_record_of_potential_close_contact = VisitRecord.objects.filter(record_datetime__date__in = dates, member_uid = potential_close_contact_uid)
            #print('===========\tNani',visit_record_of_potential_close_contact)

            # for dateX in dates:
            #     temp = VisitRecord.objects.filter(member_uid = potential_close_contact)
            #     x = potential_close_contact['member_uid']
            #     print(f'TEMP {x} ====================== \t', temp)

            if visit_record_of_potential_close_contact:

                current = visit_record_of_potential_close_contact[0]
                for visit in visit_record_of_potential_close_contact.order_by('record_datetime'):
                    #print('===========\tVisit',visit)
                    if visit.access_type == 'IN':
                        current = visit
                    else:
                        #print(visit)
                        entry_exit_pairs.append(
                            {
                                'member_uid': visit.member_uid,
                                'venue_code': visit.venue_code,
                                'time_in': current.record_datetime,
                                'time_out': visit.record_datetime
                            }
                        )

                        current = None

        entry_exit_pairs_of_infected = list() #ist(filter(lambda x: x['member_uid'] == uid, entry_exit_pairs))

        for i in entry_exit_pairs:
            #print(i['member_uid'],uid, str(i['member_uid']) == str(uid))
            if str(i['member_uid']) == str(uid):
                entry_exit_pairs_of_infected.append(i)

        print(entry_exit_pairs_of_infected)

        for entry_exit_pair in entry_exit_pairs:
            for bad_time_to_be_here in entry_exit_pairs_of_infected:
                print(entry_exit_pair['time_in'],'\t',bad_time_to_be_here['time_out'])
                if entry_exit_pair['time_in'] < bad_time_to_be_here['time_out'] and entry_exit_pair['time_out'] > bad_time_to_be_here['time_in']:
                    overlap = min( entry_exit_pair['time_out'] - bad_time_to_be_here['time_in'], bad_time_to_be_here['time_out'] - entry_exit_pair['time_in'])
                    if overlap.seconds / 360 > 0.5:
                        close_contacts.append(entry_exit_pair['member_uid'])

        return HKUMember.objects.filter(uid__in = close_contacts)



    # To-do
    # Decide on what the url looks like and how to extract parameters
    # Steps to get close contacts
    # 1. Get all access records for date-2, date-1, and date
    # 2. Group access records into IN & OUT pairs
    # 3. Find IN & OUT pairs of infected/query HKUMember
    # 4. Iterate through list of pairs and select those that overlap for more than 30 minutes


"""
Author: Peng Yinglun
This class provides the ListAPIview functionality of listing all the venues in the
database, including their venue_code, location, type and all other information.
"""
class view_all_venues(generics.ListAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

"""
Author: Peng Yinglun
This class will provide the createAPIView functionality of creating a new venue
record information. (this is done by the Task Force member and is not part of the
project sprint 1). using this, the venue info could be created.
"""
class create_venue(generics.CreateAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

"""
Author: Peng Yinglun
This class provides the retrieveAPIView functionality of displaying the records of
venues. using this, user could display a single venue.
"""
class view_venue(generics.RetrieveAPIView):
    lookup_field = 'venue_code'
    serializer_class = VenueSerializer
    def get_queryset(self, **kwargs):
        venue_code = self.kwargs['venue_code']
        queryset = Venue.objects.filter(venue_code = venue_code)
        return queryset

"""
Author: Peng Yinglun
This class provides the modify members functionality of modifying a venue info.
using this, user can modify the Venue records.
"""
class modify_venue(generics.UpdateAPIView):
    lookup_field = 'venue_code'
    serializer_class = VenueModifySerializer
    def get_queryset(self, **kwargs):
        venue_code = self.kwargs['venue_code']
        queryset = Venue.objects.filter(venue_code = venue_code)
        return queryset

"""
Author: Peng Yinglun
This class provides the destroyAPIViews functionality of deleting venues.
using this, user can edlete the existing venue records.
"""
class delete_venue(generics.DestroyAPIView):
    lookup_field = 'venue_code'
    serializer_class = VenueSerializer
    def get_queryset(self, **kwargs):
        venue_code = self.kwargs['venue_code']
        queryset = Venue.objects.filter(venue_code = venue_code)
        return queryset


"""
Author: Shao Rui
This class provides the CreateAPIView functionality of creating new member
Using this, new records of members can be created.
"""
class create_member(generics.CreateAPIView):
    queryset = HKUMember.objects.all()
    serializer_class = HKUMemberSerializer

"""
Author: Shao Rui
This class provides the ListAPIView functionality of displaying
all HKU Members' record
"""
class list_all_members(generics.ListAPIView):
    queryset = HKUMember.objects.all()
    serializer_class = HKUMemberSerializer

"""
Author: Shao Rui
This class provides the RetrievAPIView functionality of displaying
one single HKU Member's record
"""
class view_member(generics.RetrieveAPIView):
    lookup_field = 'uid'
    serializer_class = HKUMemberSerializer
    def get_queryset(self, **kwargs):
        uid = self.kwargs['uid']
        queryset = HKUMember.objects.filter(uid=uid)
        return queryset

"""
Author: Shao Rui
This class provides the UpdateAPIView functionality of modifying member records
Using this, we can modify existing HKUMember records
"""
class modify_member(generics.UpdateAPIView):
    lookup_field = 'uid'
    serializer_class = HKUMemberModifySerializer
    def get_queryset(self, **kwargs):
        uid = self.kwargs['uid']
        queryset = HKUMember.objects.filter(uid=uid)
        return queryset

"""
Author: Shao Rui
This class provides the DetroyAPIView functionality of deleting member records
Using this, we can delete existing HKUMember records
"""
class delete_member(generics.DestroyAPIView):
    lookup_field = 'uid'
    serializer_class = HKUMemberSerializer
    def get_queryset(self, *args, **kwargs):
        uid = self.kwargs['uid']
        queryset = HKUMember.objects.filter(uid=uid)
        return queryset

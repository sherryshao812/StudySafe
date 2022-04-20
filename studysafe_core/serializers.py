from os import access
from rest_framework import serializers

from .models import VisitRecord
from .models import Venue
from .models import HKUMember

# Here, we define all the custom serializers required for the API

"""
Author: Anchit Mishra

This class defines the custom serializer to be used for the VisitRecord model.
"""
class VisitRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = VisitRecord
        fields = '__all__'

"""
Author: Peng Yinglun

This class defines the custom serializer to be used for the venue model.
"""
class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'

"""
Author: Peng Yinglun

This class defines the custom serializer only for the modify purpose.
"""
class VenueModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        exclude = ['venue_code',]

"""
Author: Shao Rui

This class defines the custom serializer to be used for the HKUMember model.
"""
class HKUMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = HKUMember
        fields = '__all__'

"""
Author: Peng Yinglun

This class defines the custom serializer only for the modify purpose.
"""
class HKUMemberModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = HKUMember
        exclude = ['uid',]

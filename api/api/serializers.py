from rest_framework import serializers
from django.urls.resolvers import RegexPattern

class URLSerializer(serializers.Serializer):
    # Define fields for pattern names and URLs
    def to_representation(self, instance):
        current_domain = self.context['request'].build_absolute_uri('/')[:-1]
        
        urls = {}
        for pattern in instance:
            # if isinstance(pattern, RegexPattern):  # Checking for RegexPattern to avoid errors
            if hasattr(pattern, 'name'):
                urls[pattern.name] = f'{current_domain}/{pattern.pattern}'
            else:
                urls[str(pattern)] = f'{current_domain}/{pattern.pattern}'
        
        return urls

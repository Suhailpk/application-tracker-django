from rest_framework import serializers
from .models import *
from core.models import User
from reminder.models import Reminder
# from django.contrib.auth.models import User


# class UserSerailzer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'password')


class RegisterSerailizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password1', 'password2', 'email', 'first_name', 'last_name']




from core.models import User

class AddNewApplicationSerailzer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)  # The user field will just hold the ID
    company_id = serializers.IntegerField()
    company_name = serializers.SerializerMethodField()
    applied_status_stats = serializers.SerializerMethodField()
    status_full = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = ('id', 'user_id', 'company_id', 'company_name','applied_status_stats', 'position', 'status', 'status_full', 'salary', 'comments')


    def get_company_name(self, obj):
        company = Company.objects.filter(id=obj.company_id).first()
        return company.name if company else None
    
    def get_status_full(self, obj):
        return dict(JobApplication.STATUS_CHOICES).get(obj.status)
    
    def get_applied_status_stats(self,obj):
        status = JobApplication.objects.filter(user_id=obj.user_id).values_list('status')
        status_dict = {
            'Applied':0,
            'Interview':0,
            'Offer':0,
            'Rejected':0
        }

        for stat in status:
            if stat[0] == "AP":
                status_dict['Applied'] += 1
            elif stat[0] == "IN":
                status_dict['Interview'] += 1
            elif stat[0] == "OF":
                status_dict['Offer'] += 1
            elif stat[0] == "RE":
                status_dict['Rejected'] += 1
        
        print("stat dict final --------->", status_dict)
        cleaned_dict = {key: value for key, value in status_dict.items() if value != 0}
        print("cleaned_dict ----------->", cleaned_dict)
        return cleaned_dict


    def create(self, validated_data):
        user_id = self.context["user_id"]  # Get the user_id from the context
        # Create the JobApplication instance
        job_application = JobApplication.objects.create(user_id=user_id, **validated_data)
        # Set the companies to the job application
        job_application.save()

        Reminder.objects.create(
            job_application = job_application,
            user_id=user_id
        )

        return job_application
    


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'location', 'website', 'industry')



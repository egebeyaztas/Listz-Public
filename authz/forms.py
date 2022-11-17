from django import forms
from authz.models import Profile

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields  = ['name', 'country','bio', 'profile_picture']

    def save(self, commit=True):
        profile = super(ProfileUpdateForm, self).save(commit=False)
        profile.name = self.cleaned_data['name']
        profile.country = self.cleaned_data['country']
        profile.bio = self.cleaned_data['bio']
        profile.profile_picture = self.cleaned_data['profile_picture']
        if commit:
            profile.save()
        return profile

    

from django import forms
from models import Category, Page, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    

    
    class Meta:
        model = Category
        fields= ('name',)
        
class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text='Max allowed charectores: 128')
    url = forms.CharField(max_length=120)
    views = forms.IntegerField(widget= forms.HiddenInput, initial=0)
    
    def clean(self):
        cleand_data = self.cleaned_data
        url = cleand_data.get('url')
        
        if url and not url.startswith('http://'):
            url = "http://" + url
            cleand_data['url'] = url
        return cleand_data
    
    class Meta:
        model = Page
        exclude= ('category',)
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','email','password')
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
        

        

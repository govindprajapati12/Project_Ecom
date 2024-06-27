from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from app.models import User
# from phonenumber_field.formfields import PhoneNumberField

class SignInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    # first_name = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # last_name = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # comapany_address = forms.CharField(max_length=20, required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    # profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone_number', 'address')
                #   , 'first_name', 'last_name', 'comapany_address', 'profile_image')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})



class ProfileUpdateForm(forms.ModelForm):
    # email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    first_name = forms.CharField(max_length=2000, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=2000, widget=forms.TextInput(attrs={'class': 'form-control'}))
    company_address = forms.CharField(max_length=2000, widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('phone_number', 'address', 'first_name', 'last_name', 'company_address', 'profile_image')


class QuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=100, initial=100, label='Quantity')



# class CategorySearchForm(forms.Form):
#     query = forms.CharField(label='Search Categories', max_length=100)


#     def __init__(self, *args, **kwargs):
#         super(ProfileUpdateForm, self).__init__(*args, **kwargs)
#         # print("------args, kwargs----", args)
#         print("------self.data----", self.data.get("last_name"))
#         self.fields['email'].widget.attrs.update({'class': 'form-control'})
#         self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
#         self.fields['address'].widget.attrs.update({'class': 'form-control'})
#         self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
#         self.fields['last_name'].widget.attrs.update(self.data.get('last_name', self.instance.last_name))
#         self.fields['comapany_address'].widget.attrs.update({'class': 'form-control'})
#         self.fields['profile_image'].widget.attrs.update({'class': 'form-control'})


    # def save(self, commit=True):
    #     user = super(ProfileUpdateForm, self).save(commit=False)
    #     # print("---------", user.username, self.data)
    #     # print("-----username----", self.instance.username)
    #     user.username = self.instance.username  # Set the username from the instance
    #     if commit:
    #         user.save()
    #     return user

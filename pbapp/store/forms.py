from django import forms
from django.forms.utils import ErrorList


class Register(forms.Form):
    name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Nom'}),
        required=True,

    )
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={'class': 'form-group', 'placeholder': 'Email'}),
        required=True
    )
    passwd = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={'class': 'form-group', 'placeholder': 'Mot de passe'}),
        required=True
    )


class SearchProduct(forms.Form):
    search = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-inline'}),
        required=False
    )


class LogIn(forms.Form):
    name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'nom'}),
        required=True
    )
    passwd = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={'class': 'form-group', 'placeholder': 'Mot de passe'}),
        required=True
    )


class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])


class ChangePassword(forms.Form):
    passwd = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={'class': 'form-group', 'placeholder': 'Mot de passe'}),
        required=True
    )
    confPasswd = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={'class': 'form-group', 'placeholder': 'Confirmer mot de passe'}),
        required=True
    )



from django import forms
from kitchen.models import Dish, DishType, Cook


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        name = cleaned_data.get('name')
        dish_type = cleaned_data.get('dish_type')

        if price is not None and price < 0:
            raise forms.ValidationError("Price must be greater than or equal to 0")

        if not name:
            raise forms.ValidationError("This field is required.")

        if not dish_type:
            raise forms.ValidationError("This field is required.")

        return cleaned_data


class DishTypeForm(forms.ModelForm):
    class Meta:
        model = DishType
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')

        if not name:
            raise forms.ValidationError("Name is required")

        if DishType.objects.filter(name=name).exists():
            raise forms.ValidationError("This dish type already exists")

        return cleaned_data


class CookForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        years = cleaned_data.get('years')

        if years is not None and years < 0:
            raise forms.ValidationError("Years must be greater than or equal to 0")


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = Cook
        fields = ['username', 'email', 'password', 'years_of_experience']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

    def save(self, commit=True):
        cook = super().save(commit=False)
        cook.set_password(self.cleaned_data["password"])
        if commit:
            cook.save()
        return cook


class DishSearchForm(forms.Form):
    q = forms.CharField(label='Search', required=False)


class CookSearchForm(forms.Form):
    q = forms.CharField(required=False, label="Search Cooks")


class DishTypeSearchForm(forms.Form):
    q = forms.CharField(required=False, label="Search Dish Types")

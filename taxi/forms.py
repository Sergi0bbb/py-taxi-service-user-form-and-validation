import re

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


def validate_license_number(license_number):
    if len(license_number) != 8:
        raise ValidationError("License number length must be 8")

    if not re.match("[A-Z]{3}", license_number[:3]):
        raise ValidationError(
            "First 3 characters must be uppercase letters"
        )

    if not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits")

    return license_number


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = (
            "last_name",
            "first_name",
            "license_number",
        )

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data.get("license_number"))


class DriverLicenseCreateForm(forms.ModelForm):
    cars = forms.ModelMultipleChoiceField(
        queryset=Car.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Driver
        fields = (
            "username",
            "first_name",
            "last_name",
            "license_number",
            "cars"
        )

    def clean_license_number(self):
        return validate_license_number(self.cleaned_data.get("license_number"))


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"

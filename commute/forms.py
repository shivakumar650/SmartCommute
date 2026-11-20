from django import forms


class JourneyPlannerForm(forms.Form):
    TRANSPORT_CHOICES = (
        ("Bus", "Bus"),
        ("Car", "Car"),
        ("Bike", "Bike"),
    )

    source = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. Central Station",
        }),
    )
    destination = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. Green Park",
        }),
    )
    transport_type = forms.ChoiceField(
        choices=TRANSPORT_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    departure_time = forms.TimeField(
        widget=forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
    )

    def clean_source(self):
        source = self.cleaned_data["source"].strip()
        if len(source) < 2:
            raise forms.ValidationError("Enter a valid starting location.")
        return source

    def clean_destination(self):
        destination = self.cleaned_data["destination"].strip()
        if len(destination) < 2:
            raise forms.ValidationError("Enter a valid destination.")
        return destination

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get("source")
        destination = cleaned_data.get("destination")
        if source and destination and source.lower() == destination.lower():
            raise forms.ValidationError(
                "Starting location and destination must be different."
            )
        return cleaned_data

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


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your name",
        }),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "you@example.com",
        }),
    )
    subject = forms.CharField(
        max_length=180,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Message subject",
        }),
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 5,
            "placeholder": "Write your question or feedback",
        }),
    )

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter a valid name.")
        return name

    def clean_subject(self):
        subject = self.cleaned_data["subject"].strip()
        if len(subject) < 3:
            raise forms.ValidationError("Please enter a descriptive subject.")
        return subject

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError(
                "Please enter at least 10 characters."
            )
        return message

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class ContentGenerationForm(forms.Form):
    content_type = forms.ChoiceField(
        choices=[
            ("blog", "Blog Post"),
            ("product", "Product Description"),
            ("social", "Social Media Caption"),
        ],
        label="Content Type",
    )
    language = forms.CharField(label="Language", max_length=20)
    prompt = forms.CharField(label="Prompt", widget=forms.Textarea, max_length=5000)
    tone = forms.ChoiceField(
        choices=[("formal", "Formal"), ("casual", "Casual"), ("creative", "Creative")],
        label="Tone",
    )

from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    text_post = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['title_post',
                  'text_post',
                  'categories_post']

    def clean(self):
        cleaned_data = super().clean()
        title_post = cleaned_data.get("title_post")
        text_post = cleaned_data.get("text_post")

        if title_post == text_post:
            raise ValidationError(
                "Текст поста не должен быть идентичен заголовку."
            )

        return cleaned_data

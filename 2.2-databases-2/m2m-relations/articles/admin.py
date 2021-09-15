from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, ArticleTags, Tag

class ArticleTagsInlineFormset(BaseInlineFormSet):
    def clean(self):
        articles_edit = False
        main_tag_exists = False
        for form in self.forms:
            articles_edit |= ('is_main' in form.cleaned_data.keys())
            print(form.cleaned_data.get('is_main'))
            if form.cleaned_data.get('is_main'):
                if main_tag_exists:
                    raise ValidationError('Основным должен быть только один Тэг')
                main_tag_exists = True
        if not main_tag_exists and articles_edit:
            raise ValidationError('Хотя бы один Тэг должен быть основным')


        # scope_ids = []
        # for form in self.forms:
        #     scope_id = form.cleaned_data.get('scope_id')
        #     if scope_id is not None:
        #         if scope_id not in scope_ids:
        #             scope_ids.append(scope_id)
        #         else:
        #             raise ValidationError('Повторяющийся тэг')

        return super().clean()  # вызываем базовый код переопределяемого метода

class ArticleTagsInline(admin.TabularInline):
    model = ArticleTags
    formset = ArticleTagsInlineFormset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # list_display = ['scopes', 'scopes__is_main']
    inlines = [ArticleTagsInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [ArticleTagsInline]
    pass



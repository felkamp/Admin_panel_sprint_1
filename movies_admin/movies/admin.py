from django.contrib import admin
from .models import FilmWork, Person, Genre, PersonFilmWork


class PersonFilmWorkInline(admin.TabularInline):
    model = PersonFilmWork
    extra = 0
    autocomplete_fields = ("person", "film_work")


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "creation_date", "rating")
    fields = (
        "title",
        "type",
        "description",
        "creation_date",
        "certificate",
        "file_path",
        "rating",
        "genres",
    )

    inlines = [PersonFilmWorkInline]
    search_fields = ("title",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("fullname",)
    fields = ("first_name", "last_name")
    inlines = [PersonFilmWorkInline]

    search_fields = ("first_name", "last_name")

    @admin.display
    def fullname(self, obj):
        return obj.first_name + " " + obj.last_name


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    fields = ("name",)

    search_fields = ("name",)
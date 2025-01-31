from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import *

class CourseAdmin(ModelAdmin):
    list_display = ('id', 'title', 'price', 'sold',)
    list_display_links = ('id', 'title',)
    list_filter = ('category',)
    list_editable = ('price',)
    search_fields = ('title', 'description',)
    list_per_page = 25
    filter_horizontal = (
        'what_learnt',
        'requisite',
        'rating',
        'course_section',
        'comments',
        'resources',
        'questions',
    )

class CourseSectionAdmin(ModelAdmin):
    list_display = ('section_title', 'section_number', 'user', 'total_length')
    search_fields = ('section_title', 'user')
    filter_horizontal = ('episodes',)

class EpisodeAdmin(ModelAdmin):
    list_display = ('episode_uuid', 'title',)
    list_display_links = ('episode_uuid', 'title',)
    list_filter = ('episode_uuid',)
    search_fields = ('episode_uuid', 'content', 'title')
    list_per_page = 25
    filter_horizontal = ('resources', 'questions')

class SectorAdmin(ModelAdmin):
    list_display = ('id', 'title',)
    list_editable = ('title',)
    list_per_page = 10
    filter_horizontal = ('related_courses',)

class QuestionAdmin(ModelAdmin):
    pass

class WhatLearntAdmin(ModelAdmin):
    # Si WhatLearnt tiene campos de varios a varios, agréguelos aquí
    pass

class RequisiteAdmin(ModelAdmin):
    # Si el Requisito tiene campos de varios a varios, agréguelos aquí
    pass

# Registrar modelos con sus respectivas clases de administrador
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseSection, CourseSectionAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(CoursesLibrary)
admin.site.register(PaidCoursesLibrary)
admin.site.register(Rate)
admin.site.register(WhatLearnt, WhatLearntAdmin)
admin.site.register(Requisite, RequisiteAdmin)
admin.site.register(Resource)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Votes)
admin.site.register(Comment)

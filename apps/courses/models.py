from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.conf import settings
from apps.user.models import UserAccount as User
import uuid
from decimal import Decimal
from .helpers import get_timer
from mutagen.mp4 import MP4,MP4StreamInfoError
from django.utils import timezone
from .validators import validate_is_video
from apps.category.models import Category


def course_directory_path(instance, filename):
    return 'courses/{0}/{1}'.format(instance.title, filename)

def sector_directory_path(instance, filename):
    return 'courses/sector/{0}/{1}'.format(instance.title, filename)

def chapter_directory_path(instance, filename):
    return 'courses/{0}/{1}/{2}'.format(instance.course, instance.title, filename)

def lesson_directory_path(instance, filename):
    return 'courses/{0}/{1}/Lesson #{2}: {3}/{4}'.format(instance.course, instance.chapter, instance.lesson_number,instance.title, filename)


class WhatLearnt(models.Model):
    title = models.CharField(max_length=255, verbose_name='Título')
    user = models.CharField(max_length=255, verbose_name='Usuario')

    class Meta:
        verbose_name = 'Aprendizaje'
        verbose_name_plural = 'Aprendizajes'

    def __str__(self):
        return self.title

class Course(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')
    
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    languages = (
        ('espanol', 'Espanol'),
        ('english', 'English'),
    )

    payment = (
        ('paid', 'Paid'),
        ('free', 'Free'),
    )

    course_uuid = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID del curso')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    title = models.CharField(max_length=255, verbose_name='Título')
    thumbnail = models.ImageField(upload_to=course_directory_path, verbose_name='Miniatura')
    sales_video = models.FileField(upload_to=course_directory_path, verbose_name='Video promocional')
    description = models.TextField(verbose_name='Descripción')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    what_learnt = models.ManyToManyField('WhatLearnt', blank=True, verbose_name='Qué aprenderás')
    requisite = models.ManyToManyField('Requisite', blank=True, verbose_name='Requisitos')
    rating = models.ManyToManyField('Rate', blank=True, verbose_name='Calificaciones')
    student_rating = models.IntegerField(default=0, verbose_name='Calificación de estudiantes')
    language = models.CharField(max_length=50, choices=languages, verbose_name='Idioma')
    course_length = models.CharField(default=0, max_length=20, verbose_name='Duración del curso')
    course_section = models.ManyToManyField('CourseSection', blank=True, verbose_name='Secciones del curso')
    comments = models.ManyToManyField('Comment', blank=True, verbose_name='Comentarios')
    payment = models.CharField(max_length=100, choices=payment, default='paid', verbose_name='Tipo de pago')
    price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Precio')
    compare_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name='Precio comparativo')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Categoría')
    sold = models.IntegerField(default=0, blank=True, verbose_name='Vendidos')
    best_seller = models.BooleanField(default=False, verbose_name='Más vendido')
    resources = models.ManyToManyField('Resource', blank=True, verbose_name='Recursos')
    questions = models.ManyToManyField('Question', blank=True, verbose_name='Preguntas')
    published = models.DateTimeField(default=timezone.now, verbose_name='Fecha de publicación')
    status = models.CharField(max_length=10, choices=options, default='draft', verbose_name='Estado')

    objects = models.Manager()
    postobjects = PostObjects()

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return self.title

    def get_video(self):
        if self.thumbnail:
            return self.sales_video.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        return ''

    def get_rating(self):
        ratings=self.rating.all()
        rate=0
        for rating in ratings:
            rate+=rating.rate_number
        try:
            rate/=len(ratings)
        except ZeroDivisionError:
            rate=0
        return rate

    def get_no_rating(self):
        return len(self.rating.all())

    def get_brief_description(self):
        return self.description[:100]

    def get_total_lectures(self):
        lectures=0
        for section in self.course_section.all():
            lectures+=len(section.episodes.all())
        return lectures

    def total_course_length(self):
        length=Decimal(0.00)
        for section in self.course_section.all():
            for episode in section.episodes.all():
                length +=episode.length
        return get_timer(length)


class Rate(models.Model):
    rate_number = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)], verbose_name='Número de calificación')
    user = models.CharField(max_length=255, verbose_name='Usuario')

    class Meta:
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'





class Requisite(models.Model):
    title = models.CharField(max_length=255, verbose_name='Título')
    user = models.CharField(max_length=255, verbose_name='Usuario')

    class Meta:
        verbose_name = 'Requisito'
        verbose_name_plural = 'Requisitos'

    def __str__(self):
        return self.title


class CourseSection(models.Model):
    section_title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Título de la sección')
    section_number = models.IntegerField(blank=True, null=True, verbose_name='Número de sección')
    episodes = models.ManyToManyField('Episode', blank=True, verbose_name='Episodios')
    section_uuid = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID de la sección')
    user = models.CharField(max_length=255, verbose_name='Usuario')

    class Meta:
        ordering = ('section_number',)
        verbose_name = 'Sección del curso'
        verbose_name_plural = 'Secciones del curso'

    def __str__(self):
        return self.section_title

    def total_length(self):
        total=Decimal(0.00)
        for episode in self.episodes.all():
            total+=episode.length
        return get_timer(total,type='min')
        

class Episode(models.Model):
    episode_uuid = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID del episodio')
    title = models.CharField(max_length=255, verbose_name='Título')
    file = models.FileField(upload_to=course_directory_path, validators=[validate_is_video], verbose_name='Archivo')
    content = models.TextField(verbose_name='Contenido')
    length = models.DecimalField(max_digits=100, decimal_places=2, verbose_name='Duración')
    resources = models.ManyToManyField('Resource', blank=True, verbose_name='Recursos')
    questions = models.ManyToManyField('Question', blank=True, verbose_name='Preguntas')
    episode_number = models.IntegerField(blank=True, null=True, verbose_name='Número de episodio')
    user = models.CharField(max_length=255, verbose_name='Usuario')

    class Meta:
        ordering = ('episode_number',)
        verbose_name = 'Episodio'
        verbose_name_plural = 'Episodios'

    def __str__(self):
        return self.title

    def get_video_length(self):
        try:
            video=MP4(self.file)
            return video.info.length
        except MP4StreamInfoError:
            return 0.0

    def get_video_length_time(self):
        return get_timer(self.length)

    def save(self,*args, **kwargs):
        self.length=self.get_video_length()
        return super().save(*args, **kwargs)


class Question(models.Model):
    question_uuid = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID de la pregunta')
    user = models.CharField(max_length=255, verbose_name='Usuario')
    title = models.CharField(max_length=100, verbose_name='Título')
    body = models.TextField(verbose_name='Contenido')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    update_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de actualización')
    has_accepted_answer = models.BooleanField(default=False, verbose_name='Tiene respuesta aceptada')

    class Meta:
        ordering = ('-created_date',)
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'

    def __str__(self):
        return self.title

    def get_answers_count(self):
        return Answer.objects.filter(question=self).count()

    def get_answers(self):
        return Answer.objects.filter(question=self)


class Answer(models.Model):
    answer_uuid = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID de la respuesta')
    user = models.CharField(max_length=255, verbose_name='Usuario')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Pregunta')
    body = models.TextField(verbose_name='Contenido')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    update_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de actualización')
    votes = models.IntegerField(default=0, verbose_name='Votos')
    is_accepted_answer = models.BooleanField(default=False, verbose_name='Es respuesta aceptada')

    class Meta:
        ordering = ('-created_date',)
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'

    def __str__(self):
        return self.user

    def calculate_votes(self):
        u_votes = Votes.objects.filter(answer=self, vote='U').count()
        d_votes = Votes.objects.filter(answer=self, vote='D').count()
        self.votes = u_votes - d_votes
        self.save()
        return self.votes


VOTES_CHOICES = (
    ('U', 'Up Vote'),
    ('D', 'Down Vote'),
)

class Votes(models.Model):
    user = models.CharField(max_length=255, verbose_name='Usuario')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_votes', verbose_name='Respuesta')
    vote = models.CharField(choices=VOTES_CHOICES, max_length=1, verbose_name='Voto')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')

    class Meta:
        ordering = ('-date',)
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'


class Resource(models.Model):
    title = models.CharField(max_length=255, verbose_name='Título')
    file = models.FileField(upload_to=course_directory_path, blank=True, null=True, verbose_name='Archivo')
    url = models.URLField(blank=True, null=True, verbose_name='URL')
    user = models.CharField(max_length=255, verbose_name='Usuario')

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.file.url


class Comment(models.Model):
    user = models.CharField(max_length=255, verbose_name='Usuario')
    message = models.TextField(verbose_name='Mensaje')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'


class Sector(models.Model):
    title = models.CharField(max_length=255, verbose_name='Título')
    sub_title = models.CharField(max_length=255, verbose_name='Subtítulo')
    description = models.TextField(verbose_name='Descripción')
    sector_uuid = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID del sector')
    related_courses = models.ManyToManyField('Course', blank=True, verbose_name='Cursos relacionados')
    thumbnail = models.ImageField(upload_to=sector_directory_path, verbose_name='Miniatura')

    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectores'

    def __str__(self):
        return self.title

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        return ''


class CoursesLibrary(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    courses = models.ManyToManyField(Course, blank=True, verbose_name='Cursos')

    class Meta:
        verbose_name = 'Biblioteca de cursos marcados'
        verbose_name_plural = 'Bibliotecas de cursos marcados'

    def __str__(self):
        return self.author.account



class PaidCoursesLibrary(models.Model):
	author =  models.ForeignKey(User, on_delete=models.CASCADE)
	courses = models.ManyToManyField(Course, blank=True)

	class Meta:
		verbose_name_plural="Purchased Courses Library"

	def __str__(self):
		return self.author.account
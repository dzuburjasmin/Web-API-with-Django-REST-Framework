from django.db import models
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Book(models.Model):
    publication_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    authors = models.CharField(max_length=100, blank=True, default='')
    publisher = models.CharField(max_length=100, blank=True, default='')
    number_of_pages = models.IntegerField(max_length=5000, blank=True, default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        ordering = ['publication_date']

 def save(self, *args, **kwargs):
            """
            Use the `pygments` library to create a highlighted HTML
            representation of the code snippet.
            """
            lexer = get_lexer_by_name(self.language)
            linenos = 'table' if self.linenos else False
            options = {'title': self.title} if self.title else {}
            formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                      full=True, **options)
            self.highlighted = highlight(self.code, lexer, formatter)
            super(Book, self).save(*args, **kwargs)
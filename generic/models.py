from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageBlock
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
# from wagtail.images.edit_handlers import ImageChooserPanel # DEPRECATED


@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, blank=True)
    company_url = models.URLField(blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("company_name"),
        FieldPanel("company_url"),
        FieldPanel("image"),
    ]

    def __str__(self) -> str:
        return self.name


class GenericPage(Page):
    banner_title = models.CharField(
        max_length=100,
        default="Welcome to my generic page",
    )
    introduction = models.TextField(
        blank=True,
    )
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",  # No backward relation
    )
    author = models.ForeignKey(
        Author,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    body = StreamField(
        [
            ("heading", blocks.CharBlock()), # template="heading_block.html"
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("banner_title"),
        FieldPanel("introduction"),
        FieldPanel("banner_image"),
        FieldPanel("author"),
        FieldPanel("body"),
        # ImageChooserPanel(DEPRECATED),
        # SnippetChooserPanel(DEPRECATED)
    ]

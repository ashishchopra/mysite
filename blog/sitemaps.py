from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from taggit.models import Tag

from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated


class TagSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        # Return all tags that are actually used by posts
        return Tag.objects.filter(taggit_taggeditem_items__isnull=False).distinct()

    def lastmod(self, obj):
        latest_post = Post.published.filter(tags__in=[obj]).order_by('-updated').first()
        return latest_post.updated if latest_post else None

    def location(self, obj):
        # Generate the URL for each tag
        return reverse('blog:post_list_by_tag', args=[obj.slug])
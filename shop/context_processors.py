#Using Context Processor to make category links/menu links function available throughout the website so navbar can show all categories

from . models import Category


def menu_links(request):
	links = Category.objects.all()
	return dict(links=links)
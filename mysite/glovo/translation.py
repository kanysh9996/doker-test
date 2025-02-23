from .models import Category, Store, Product, Contact
from modeltranslation.translator import TranslationOptions, register


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name', )


@register(Store)
class StoreTranslationOptions(TranslationOptions):
    fields = ('store_name', 'description')


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'description')


@register(Contact)
class ContactTranslationOptions(TranslationOptions):
    fields = ('title',)


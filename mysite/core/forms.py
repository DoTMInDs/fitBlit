from django import forms
from django.forms import modelformset_factory
from blog.models import Item,ItemImage

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "title",
            "market_price",
            "price",
            "description",
            "image",
            "location",
            "contact",
            "item_status",
            "item_type"
        ]
   
class ItemEditForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "title",
            "market_price",
            "price",
            "description",
            "image",
            "location",
            "contact",
            "item_status",
            "item_type"
        ]

ItemImageFormSet = modelformset_factory(
    ItemImage,
    fields=('image',),
    extra=3,  # Allows up to 5 images
    can_delete=True
)

# class ItemImageForm(forms.ModelForm):
#     image = forms.ImageField(
#         label="Image",
#         widget=forms.FileInput(attrs={"multiple": True}),
#     )
#     class Meta:
#         model = ItemImage
#         fields = ('image',)
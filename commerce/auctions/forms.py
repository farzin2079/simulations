from django.forms import ModelForm
from .models import Listing, Categorys

class ListingForms(ModelForm):
    class Meta:
        model = Listing
        fields = [ 'title', 'image', 'description', 'base_price', 'category']
        
    def __init__(self, *args, **kwargs):
        super(ListingForms, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({ 'placeholder': field.label})
            
from django import forms
from .models import Ticket

class TicketPurchaseForm(forms.ModelForm):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Ticket
        fields = ['quantity']
    
    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)
        
        if self.event:
            # Set max quantity based on available tickets
            max_quantity = min(10, self.event.available_tickets)
            self.fields['quantity'].widget.attrs['max'] = max_quantity
            self.fields['quantity'].validators[0].limit_value = max_quantity

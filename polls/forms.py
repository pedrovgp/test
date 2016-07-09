from django import forms

class ContactForm(forms.Form):
#    subject = forms.CharField(max_length=100)
#    message = forms.CharField(widget=forms.Textarea)
    CHOICES = ((x,x) for x in range(8))
    male_num = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    CHOICES2 = ((x,x) for x in range(8))
    female_num = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES2)
    sender = forms.EmailField()
#    cc_myself = forms.BooleanField(required=False)

class AcceptForm(forms.Form):
    accepted = forms.BooleanField(required=False)


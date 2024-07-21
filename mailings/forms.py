# from django import forms
# from mailings.models import Client,Message,Newsletter,Logs
#
#
#
# class NewsletterForm(forms.ModelForm):
#     class Meta:
#         model = Newsletter
#         fields = ('start_time', 'end_time','periodicity','status','client','message')
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'
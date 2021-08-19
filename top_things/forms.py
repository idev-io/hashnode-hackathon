from django import forms
from .models import Thing, Category


# Create Thing Form 
class ThingCreateForm(forms.ModelForm):

    BEGINNER = 'Beginner'
    INTERMEDIATE = 'Intermediate'
    ADVANCED = 'Advanced'

    RANK_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced')
    ]

    category = forms.ModelChoiceField(label='Category',
                          queryset=Category.objects.all().order_by('-id'),
                          widget=forms.Select(attrs={
                            'class': 'custom-select',
                            'default':'Choose One',
                            'error_messages': 'Please, select category'
                          },),
                          required=True,
                          initial='--Choose Category--',)


    rank = forms.CharField(max_length=12,
                          label='Level', 
                          widget=forms.Select(attrs={
                            'class': 'custom-select',
                            'error_messages': 'Choose one of this choices'
                          },choices=RANK_CHOICES,))


    title = forms.CharField(max_length=100, 
                          min_length=3,
                          widget=forms.TextInput(attrs={
                            'class': 'form-control form-control-md',
                            'type': 'text',
                            'help_text':"At least 3 letters",
                            'placeholder':"Title",
                            'unique':True,
                          }),
                          required=True,
                          label='Title',
                          strip=True,
                          error_messages={'required': 'Title is required with at least 3 letters'})


    subtitle = forms.CharField(max_length=200, 
                          min_length=5,
                          widget=forms.TextInput(attrs={
                            'class': 'form-control form-control-md',
                            'type': 'text',
                            'help_text':"At least 5 letters",
                            'placeholder':"Subtitle",
                          }),
                          required=True,
                          label='Subtitle',
                          strip=True,
                          error_messages={'required': 'Subtitle is required with at least 5 letters'})


    link = forms.CharField(max_length=1000, 
                          min_length=20,
                          widget=forms.TextInput(attrs={
                            'class': 'form-control form-control-md',
                            'type': 'text',
                            'help_text':"At least 20 letters",
                            'placeholder':"Link",
                          }),
                          required=True,
                          label='Link',
                          strip=True,
                          error_messages={'required': 'Link is required'})
    

    picture = forms.ImageField(label='Image',
                               widget=forms.FileInput(attrs={
                                    'class': 'custom-file',
                                    'type': 'file',
                                    'placeholder':"Choose Image",
                                }),
                                required=True,
                                error_messages={'required': 'Image is required'})


    description = forms.CharField(label='Description',
                                  widget=forms.Textarea(attrs={
                                        'class': 'form-control form-control-md',
                                        'type': 'text',
                                        'placeholder':"Description",
                                    }),
                                    required=True,
                                    strip=True,
                                    error_messages={'required': 'Description is required'})

    
    slug = forms.CharField(min_length=3,
                          widget=forms.TextInput(attrs={
                            'class': 'form-control form-control-md',
                            'type': 'text',
                            'placeholder':"Slug",
                            'unique':True,
                          }),
                          required=True,
                          label='Slug',
                          strip=True,
                          error_messages={'required': 'Slug is required'})

    class Meta:
        model = Thing
        fields = '__all__'
        exclude = ['user']




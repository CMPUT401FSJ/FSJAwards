from .models import Comment
from .forms_modelform import ModelForm

class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('adjudicator', 'application', 'comment_text')
        
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)   
        
        
class CommentRestrictedForm(ModelForm):
    
    class Meta:
        model = Comment
        fields = ('comment_text',)
            
    def __init__(self, *args, **kwargs):
        super(CommentRestrictedForm, self).__init__(*args, **kwargs)

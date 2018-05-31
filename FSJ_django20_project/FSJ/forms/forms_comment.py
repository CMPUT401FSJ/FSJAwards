"""Contains all Django ModelForms related to the Comment model"""

from ..models import Comment
from .forms_modelform import ModelForm

class CommentForm(ModelForm):
    """Unrestricted Comment form, which is only used by the program itself and not any user"""
    class Meta:
        model = Comment
        fields = ('adjudicator', 'application', 'comment_text')
        
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)   
        
        
class CommentRestrictedForm(ModelForm):
    """Restricted Comment form used by adjudicators to comment on applications"""
    class Meta:
        model = Comment
        fields = ('comment_text',)
            
    def __init__(self, *args, **kwargs):
        super(CommentRestrictedForm, self).__init__(*args, **kwargs)

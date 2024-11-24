from django import forms
from django.core.validators import FileExtensionValidator

from .models import UploadModel


class UploadFileForm(forms.ModelForm):
    input_video = forms.FileField(allow_empty_file=False, required=True, label="", widget=forms.FileInput({"class":"custom-file-input mb-3", "for":"inputGroupFile01","id":"inputGroupFile01", "aria-describedby":"inputGroupFileAddon01"}), validators=[FileExtensionValidator(["webm","mkv","flv","vob","ogv","ogg","webm","drc","gif","gifv","mng","avi","mts","m2ts","ts","mov","qt","wmv","yuv","rm","rmvb","viv","asf","amv","mp4","m4p","mpg","mp2","mpeg","mpe","mpv","mpg","mpeg","m2v","m4v","svi","3gp","3g2","mxf","roq","nsv","f4p","f4v","f4a","f4b"], "This file is not valid")])

    class Meta:
        model = UploadModel
        fields = ("input_video",)










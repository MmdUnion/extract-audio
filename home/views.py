import os
import re

from django.conf import settings
from django.core.paginator import Paginator
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import resolve
from django.utils.translation import activate
from django.views.generic import View

from .forms import UploadFileForm
from .models import BlogModel, UploadModel
from .tasks import proccessing_to_convert_video


class HomeView(View):
    template_name = "home/home_view.html"
    form_class = UploadFileForm

    def get(self, request):
        return render(request, self.template_name, context={"form":self.form_class})



class UploadView(View):
    template_name = "home/home_view.html"
    form_class = UploadFileForm

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save()
            proccessing_to_convert_video.delay(new_form.pk)
            return JsonResponse({"status":"ok", "file_id":new_form.download_url})

        return JsonResponse({"status":"fail"})




class StatusView(View):
    def post(self, request):
        try:
            prepare_file_id = re.match(r"^([a-z0-9]{8}-?[a-z0-9]{4}-?[a-z0-9]{4}-?[a-z0-9]{4}-?[a-z0-9]{12}$)", request.POST['file_id']).group(1)
        except:
            prepare_file_id = None
        if prepare_file_id != None:
            model = UploadModel.objects.filter(download_url=prepare_file_id)
            if model:
                model = model[0]
                new_dict = {"status":model.status}
                if model.status == "Success":
                    new_dict['audio_url'] = f"download/{model.download_url}"
                    new_dict['mime_type'] = model.mime_type
                return JsonResponse(new_dict)
        return JsonResponse({"status":"File not found"})



class DownloadView(View):
    def get(self, request, *args, **kwargs):
        model = get_object_or_404(UploadModel, download_url=kwargs.get("file_id"))
        if model and model.audio_url:
            base_name = os.path.basename(model.audio_url.path)
            file_name = f"extract-audio_{base_name}"

            with open(model.audio_url.path, "rb") as read_file:
                file_read = read_file.read()

            response = HttpResponse(file_read, content_type=model.mime_type)
            response['Content-Length'] = len(file_read)
            response['Content-Type'] = model.mime_type

            response['Content-Disposition'] = f'attachment; filename="{file_name}"'

            return response

        raise Http404


class AboutUsView(View):
    template_name = "home/about_us_view.html"

    def get(self, request):
        return render(request, self.template_name)

class ContactUsView(View):
    template_name = "home/contact_us_view.html"

    def get(self, request):
        return render(request, self.template_name)

class CreditView(View):
    template_name = "home/credit.html"

    def get(self, request):
        return render(request, self.template_name)









class BlogView(View):
    template_name = "home/blog_view.html"

    def get(self, request):
        page_number = request.GET.get("page", 1)

        get_blogs = BlogModel.objects.filter(published=True).order_by("-created_at")

        paginator = Paginator(get_blogs, 9)

        get_page_obj = paginator.get_page(page_number)


        return render(request, self.template_name, {"page_obj":get_page_obj})






class BlogContentView(View):
    template_name = "home/blog_content_view.html"
    get_post_id = None
    get_post_name = None
    def setup(self, request, *args, **kwargs):
        self.get_post_id = kwargs.get("post_id")
        self.get_post_name = kwargs.get("post_name")
        if self.get_post_id and self.get_post_name:
            return super().setup(request, *args, **kwargs)


        raise Http404

    def get(self, *args, **kwargs):
        get_blog = get_object_or_404(BlogModel, published=True, id=self.get_post_id, slug=self.get_post_name)
        if get_blog:
            get_last = BlogModel.objects.filter(published=True).order_by("-created_at")[:3]

            return render(*args, self.template_name, {"content":get_blog, "content_data":get_last})



class ChangeLanguage(View):
    def get(self, request):
        get_next = self.request.GET.get("next")
        get_language = self.request.GET.get("change")
        if not get_next or not get_language:
            raise Http404

        can_redirect = False
        for any_language in settings.LANGUAGES:
            if any_language[0] == get_language:
                can_redirect = True
                break
        if not can_redirect:
            raise Http404


        if can_redirect:
            activate(get_language)
            try:
                resolve(get_next)
            except:
                raise Http404
            return redirect(get_next)
        raise Http404




class WebmToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"WEBM to MP3 Converter Online - Extract Audio",
            "description":r"Convert WEBM to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"WEBM to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)


class MkvToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"MKV to MP3 Converter Online - Extract Audio",
            "description":r"Convert MKV to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"MKV to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)



class FlvToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"FLV to MP3 Converter Online - Extract Audio",
            "description":r"Convert FLV to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"FLV to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)





class VobToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"VOB to MP3 Converter Online - Extract Audio",
            "description":r"Convert VOB to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"VOB to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)







class OgvToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"OGV to MP3 Converter Online - Extract Audio",
            "description":r"Convert OGV to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"OGV to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)




class OggToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"OGG to MP3 Converter Online - Extract Audio",
            "description":r"Convert OGG to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"OGG to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)




class DrcToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"DRC to MP3 Converter Online - Extract Audio",
            "description":r"Convert DRC to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"DRC to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)





class GifToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"GIF to MP3 Converter Online - Extract Audio",
            "description":r"Convert GIF to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"GIF to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)








class GifvToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"GIFV to MP3 Converter Online - Extract Audio",
            "description":r"Convert GIFV to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"GIFV to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)




class MngvToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"MNG to MP3 Converter Online - Extract Audio",
            "description":r"Convert MNG to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"MNG to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)





class AviToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"AVI to MP3 Converter Online - Extract Audio",
            "description":r"Convert AVI to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"AVI to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)





class MtsToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"MTS to MP3 Converter Online - Extract Audio",
            "description":r"Convert MTS to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"MTS to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)





class RoqToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"ROQ to MP3 Converter Online - Extract Audio",
            "description":r"Convert ROQ to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"ROQ to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)





class M2tsToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"M2TS to MP3 Converter Online - Extract Audio",
            "description":r"Convert M2TS to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"M2TS to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)





class TsToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"TS to MP3 Converter Online - Extract Audio",
            "description":r"Convert TS to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"TS to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)





class QtToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"QT to MP3 Converter Online - Extract Audio",
            "description":r"Convert QT to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"QT to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)





class MovToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"MOV to MP3 Converter Online - Extract Audio",
            "description":r"Convert MOV to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"MOV to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)





class RmvbToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"RMVB to MP3 Converter Online - Extract Audio",
            "description":r"Convert RMVB to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"RMVB to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)





class RmToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"RM to MP3 Converter Online - Extract Audio",
            "description":r"Convert RM to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"RM to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)




class WmvToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"WMV to MP3 Converter Online - Extract Audio",
            "description":r"Convert WMV to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"WMV to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)




class AmvToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"AMV to MP3 Converter Online - Extract Audio",
            "description":r"Convert AMV to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"AMV to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)




class YuvToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"YUV to MP3 Converter Online - Extract Audio",
            "description":r"Convert YUV to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"YUV to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)




class AsfToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"ASF to MP3 Converter Online - Extract Audio",
            "description":r"Convert ASF to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"ASF to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)




class Mp4ToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"MP4 to MP3 Converter Online - Extract Audio",
            "description":r"Convert MP4 to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"MP4 to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)




class M4pToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"M4P to MP3 Converter Online - Extract Audio",
            "description":r"Convert M4P to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"M4P to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)




class MpgToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"MPG to MP3 Converter Online - Extract Audio",
            "description":r"Convert MPG to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"MPG to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)




class Mp2ToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"MP2 to MP3 Converter Online - Extract Audio",
            "description":r"Convert MP2 to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"MP2 to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)



class MpegToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"MPEG to MP3 Converter Online - Extract Audio",
            "description":r"Convert MPEG to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"MPEG to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)



class MpeToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"MPE to MP3 Converter Online - Extract Audio",
            "description":r"Convert MPE to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"MPE to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)



class MpvToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"MPV to MP3 Converter Online - Extract Audio",
            "description":r"Convert MPV to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"MPV to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)



class M2vToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"M2V to MP3 Converter Online - Extract Audio",
            "description":r"Convert M2V to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"M2V to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)



class M4vToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"M4V to MP3 Converter Online - Extract Audio",
            "description":r"Convert M4V to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"M4V to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)



class SviToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"SVI to MP3 Converter Online - Extract Audio",
            "description":r"Convert SVI to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"SVI to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)


class Th3gpToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"3GP to MP3 Converter Online - Extract Audio",
            "description":r"Convert 3GP to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"3GP to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)


class Th3g2ToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"3G2 to MP3 Converter Online - Extract Audio",
            "description":r"Convert 3G2 to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"3G2 to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)


class MxfToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"MXF to MP3 Converter Online - Extract Audio",
            "description":r"Convert MXF to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"MXF to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)


class NsvToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"NSV to MP3 Converter Online - Extract Audio",
            "description":r"Convert NSV to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"NSV to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)


class F4pToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"F4p to MP3 Converter Online - Extract Audio",
            "description":r"Convert F4p to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"F4p to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)


class F4vToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"F4v to MP3 Converter Online - Extract Audio",
            "description":r"Convert F4v to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"F4v to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)


class F4aToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"F4a to MP3 Converter Online - Extract Audio",
            "description":r"Convert F4a to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"F4a to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)


class F4bToMp3(View):
    template_name = "home/other_tools.html"
    form_class = UploadFileForm
    def get(self, request):
        context = {
            "title":"F4b to MP3 Converter Online - Extract Audio",
            "description":r"Convert F4b to MP3 online and 100% free using Extract-Audio tool",
            "HeaderName":"F4b to MP3 Converter",
            "form":self.form_class
        }
        return render(request, self.template_name, context)




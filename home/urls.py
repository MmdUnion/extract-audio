
from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home_view"),
    path("language/", views.ChangeLanguage.as_view(), name="change_language"),
    path("upload/", views.UploadView.as_view(), name="upload_view"),
    path("status/", views.StatusView.as_view(), name="status_view"),
    path("download/<uuid:file_id>", views.DownloadView.as_view(), name="download_view"),
    path("about-us/", views.AboutUsView.as_view(), name="about_us_view"),
    path("contact-us/", views.ContactUsView.as_view(), name="contact_us_view"),
    path("blog/", views.BlogView.as_view(), name="blog_view"),
    path("blog/<int:post_id>/<slug:post_name>/", views.BlogContentView.as_view(), name="blog_content_view"),
    path("credits/", views.CreditView.as_view(), name="credit_view"),



    # Other tool page routes
    path("webm-to-mp3/", views.WebmToMp3.as_view(), name="webm_to_mp3"),
    path("mkv-to-mp3/", views.MkvToMp3.as_view(), name="mkv_to_mp3"),
    path("flv-to-mp3/", views.FlvToMp3.as_view(), name="flv_to_mp3"),
    path("vob-to-mp3/", views.VobToMp3.as_view(), name="vob_to_mp3"),
    path("ogv-to-mp3/", views.OgvToMp3.as_view(), name="ogv_to_mp3"),
    path("ogg-to-mp3/", views.OggToMp3.as_view(), name="ogg_to_mp3"),
    path("drc-to-mp3/", views.DrcToMp3.as_view(), name="drc_to_mp3"),
    path("gif-to-mp3/", views.GifToMp3.as_view(), name="gif_to_mp3"),
    path("gifv-to-mp3/", views.GifvToMp3.as_view(), name="gifv_to_mp3"),
    path("mng-to-mp3/", views.MngvToMp3.as_view(), name="mng_to_mp3"),
    path("avi-to-mp3/", views.AviToMp3.as_view(), name="avi_to_mp3"),
    path("mts-to-mp3/", views.MtsToMp3.as_view(), name="mts_to_mp3"),
    path("roq-to-mp3/", views.RoqToMp3.as_view(), name="roq_to_mp3"),
    path("m2ts-to-mp3/", views.M2tsToMp3.as_view(), name="m2ts_to_mp3"),
    path("ts-to-mp3/", views.TsToMp3.as_view(), name="ts_to_mp3"),
    path("qt-to-mp3/", views.QtToMp3.as_view(), name="qt_to_mp3"),
    path("mov-to-mp3/", views.MovToMp3.as_view(), name="mov_to_mp3"),
    path("rmvb-to-mp3/", views.RmvbToMp3.as_view(), name="rmvb_to_mp3"),
    path("rm-to-mp3/", views.RmToMp3.as_view(), name="rm_to_mp3"),
    path("wmv-to-mp3/", views.WmvToMp3.as_view(), name="wmv_to_mp3"),
    path("amv-to-mp3/", views.AmvToMp3.as_view(), name="amv_to_mp3"),
    path("yuv-to-mp3/", views.YuvToMp3.as_view(), name="yuv_to_mp3"),
    path("asf-to-mp3/", views.AsfToMp3.as_view(), name="asf_to_mp3"),
    path("mp4-to-mp3/", views.Mp4ToMp3.as_view(), name="mp4_to_mp3"),
    path("m4p-to-mp3/", views.M4pToMp3.as_view(), name="m4p_to_mp3"),
    path("mpg-to-mp3/", views.MpgToMp3.as_view(), name="mpg_to_mp3"),
    path("mp2-to-mp3/", views.Mp2ToMp3.as_view(), name="mp2_to_mp3"),
    path("mpeg-to-mp3/", views.MpegToMp3.as_view(), name="mpeg_to_mp3"),
    path("mpe-to-mp3/", views.MpeToMp3.as_view(), name="mpe_to_mp3"),
    path("mpv-to-mp3/", views.MpvToMp3.as_view(), name="mpv_to_mp3"),
    path("m2v-to-mp3/", views.M2vToMp3.as_view(), name="m2v_to_mp3"),
    path("m4v-to-mp3/", views.M4vToMp3.as_view(), name="m4v_to_mp3"),
    path("svi-to-mp3/", views.SviToMp3.as_view(), name="svi_to_mp3"),
    path("3gp-to-mp3/", views.Th3gpToMp3.as_view(), name="3gp_to_mp3"),
    path("3g2-to-mp3/", views.Th3g2ToMp3.as_view(), name="3g2_to_mp3"),
    path("mxf-to-mp3/", views.MxfToMp3.as_view(), name="mxf_to_mp3"),
    path("nsv-to-mp3/", views.NsvToMp3.as_view(), name="nsv_to_mp3"),
    path("f4p-to-mp3/", views.F4pToMp3.as_view(), name="f4p_to_mp3"),
    path("f4v-to-mp3/", views.F4vToMp3.as_view(), name="f4v_to_mp3"),
    path("f4a-to-mp3/", views.F4aToMp3.as_view(), name="f4a_to_mp3"),
    path("f4b-to-mp3/", views.F4bToMp3.as_view(), name="f4b_to_mp3"),

]






from celery import chain

from .forms import YoutubeUrlForm
from .tasks import download_video, mp4_to_mp3, send_email
from .utils.helpers import get_client_ip, time_until_midnight, video_is_available

from youtube_downloader import settings
from website.models import Statistics
from django.shortcuts import render


SUCCESS_MSG = 'Email with the link to the file is on the way to your email'
DOWNLOAD_LIMIT_MSG = 'Daily limit reached! Try again tomorrow.'
LINK_ERR_MSG = 'Check the link for errors, can\'t find the video!'


def index(request):
    form = YoutubeUrlForm()
    ip = get_client_ip(request)
    stats, created = Statistics.objects.get_or_create(ip=ip)
    daily_downloads = stats.daily_downloads
    time_left_until_next_dl = time_until_midnight()

    if request.method == 'POST':
        form = YoutubeUrlForm(request.POST)
        if form.is_valid():
            youtube_link = form.cleaned_data['link']
            email = form.cleaned_data['email']
            if video_is_available(youtube_link):
                if stats.daily_downloads <= settings.DAILY_LIMIT:
                    dl_task = chain(download_video.s(youtube_link),
                                    mp4_to_mp3.s(),
                                    send_email.s(email))
                    dl_task.delay()
                    stats.daily_downloads += 1
                    stats.save()
                    success_msg = SUCCESS_MSG
                    form = YoutubeUrlForm()
                else:
                    form_errors_limit = DOWNLOAD_LIMIT_MSG
            else:
                form_errors_broken_link = LINK_ERR_MSG
    return render(request, 'website/index.html', locals())

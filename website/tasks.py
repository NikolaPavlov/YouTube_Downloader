from __future__ import absolute_import, unicode_literals

import os
import uuid

import sendgrid
import moviepy.editor as mp

from celery import shared_task
from pytube import YouTube
from sendgrid.helpers.mail import Content, Email, Mail

from youtube_downloader import settings
from .utils.helpers import slugify


@shared_task
def download_video(youtube_link):
    '''
    FIRST CELERY TASK
    download the video and return it's filename + uuid4
    '''
    yt = YouTube(youtube_link)
    yt.streams \
        .filter(progressive=True, file_extension='mp4') \
        .order_by('resolution') \
        .desc() \
        .first() \
        .download(settings.MEDIA_ROOT, filename=slugify(yt.title))

    return slugify(yt.title) + '***' + str(uuid.uuid4())


@shared_task
def mp4_to_mp3(filename):
    '''
    SECOND CELERY TASK
    strip spaces from the filename and remove uuid4 part
    convert it from mp4 to mp3
    remove the mp4 and return filename.mp3 string
    '''
    filename = filename.split('***')[0]
    mp4_file_name = filename + '.mp4'
    mp4_file = os.path.join(settings.MEDIA_ROOT, mp4_file_name)
    if os.path.exists(mp4_file):
        f = mp.AudioFileClip(mp4_file)
        mp3_file_name = filename + '.mp3'
        mp3_file = os.path.join(settings.MEDIA_ROOT, mp3_file_name)
        f.write_audiofile(mp3_file)
        os.remove(mp4_file)

        if mp3_file_name is None:
            raise Exception('FAIL NONE mp3_file_name in mp4_to_mp3')
        return str(mp3_file_name)


@shared_task
def send_email(filename, email):
    '''
    THIRD CELERY TASK
    '''
    link = "<a href='{}{}'>{}</a>".format(
        settings.URL_HOST, settings.MEDIA_URL + filename, filename)

    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
    from_email = Email('youtube_convertor@gmail')
    subject = filename
    to_email = Email(email)
    content = Content('text/html', link)
    mail = Mail(from_email, subject, to_email, content)
    sg.client.mail.send.post(request_body=mail.get())

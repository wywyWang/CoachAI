import os

def store(videofile):
    if videofile.filename:
        base_filename = os.path.basename(videofile.filename)
        video_folder = './uploadvideo/'
        if not os.path.isdir(video_folder):
            os.mkdir(video_folder)
        video_path = video_folder + base_filename
        open(video_path, 'wb').write(videofile.file.read())
        message = 'The file "' + base_filename + '" was uploaded successfully'
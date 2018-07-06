import six.moves.urllib as urllib
from pathlib import Path
import jsonlines
import click
import tarfile
import os
import sys


root = Path(__file__).parent
label_map_path = root / '..' / 'cartoonify' / 'app' / 'label_mapping.jsonl'
download_path = root / '..' / 'cartoonify' / 'downloads'
quickdraw_dataset_url = 'https://storage.googleapis.com/quickdraw_dataset/full/binary/'
tensorflow_model_download_url = 'http://download.tensorflow.org/models/object_detection/'
tensorflow_model_name = 'ssd_mobilenet_v1_coco_2017_11_17'
model_path = download_path / 'detection_models' / tensorflow_model_name / 'frozen_inference_graph.pb'


def main():
    download_drawing_dataset()
    download_tensorflow_model()
    print('finished')


def download_drawing_dataset():
    try:
        path = download_path / 'drawing_dataset'
        with jsonlines.open(str(label_map_path), mode='r') as reader:
            category_mapping = reader.read()
        print('checking whether drawing files already exist...')
        drawing_categories = ['face', 't-shirt', 'pants'] + category_mapping.values()
        missing_files = [file for file in drawing_categories if not Path(path / Path(file).with_suffix('.bin')).exists()]
        if missing_files:
            print('{} drawing files missing, downloading the following files: '.format(len(missing_files)))
            for f in missing_files:
                print(f)
            download_recurse(quickdraw_dataset_url, path, missing_files)
    except IOError as e:
        print('label_mapping.jsonl not found')


def download_tensorflow_model():
    print('checking if tensorflow model exists...')
    if not model_path.exists():
        print('tensorflow model missing, downloading the following file: \n {}'.format(str(model_path)))
        filename = tensorflow_model_name + '.tar.gz'
        opener = urllib.request.URLopener()
        opener.retrieve(tensorflow_model_download_url + filename, filename)
        print('extracting model from tarfile...')
        tar_file = tarfile.open(filename)
        for file in tar_file.getmembers():
            file_name = os.path.basename(file.name)
            if 'frozen_inference_graph.pb' in file_name:
                tar_file.extract(file, path=str(model_path.parents[1]))


def download(url, filename, path):
    """download file @ specified url and save it to path
    """
    try:
        if not Path(path).exists():
            Path(path).mkdir()
        fpath = Path(path) / filename
        opener = urllib.request.URLopener()
        opener.retrieve(url, str(fpath))
        return fpath
    except (urllib.error.HTTPError, urllib.error.URLError):
        print('could not download file: {}'.format(filename))


def download_recurse(url, path, filenames):
    """download files from url

    :param str url: the url to download from, ended with a '/'
    :param str path: the directory to save the files to
    :param list files: list of filenames to download
    """
    path = Path(path)
    with click.progressbar(filenames, label='downloading drawing dataset:') as files:
        for file in files:
            site = url + file.replace(' ', '%20') + '.bin'
            fpath = download(site, file + '.bin', path)


def load_categories(path):
    files = Path(path).glob('*.bin')
    categories = [f.stem for f in files]
    return categories

if __name__=='__main__':
    main()
    sys.exit()
# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['Config', 'config', 'download_url']

# Cell
import os
from pathlib import Path
from zipfile import ZipFile,ZIP_LZMA

# Cell
class Config:
    config_path = Path(os.getenv('FRENCHTEXT_HOME', '~/.frenchtext')).expanduser()

    def __init__(self):
        self.config_path.mkdir(parents=True, exist_ok=True)
        self.create_config()
        for key in self.d:
            Path(self.d[key]).mkdir(parents=True, exist_ok=True)

    def __getitem__(self,k):
        k = k.lower()
        if k not in self.d: k = k+'_path'
        return Path(self.d[k])

    def __getattr__(self,k):
        if k=='d': raise AttributeError
        return self[k]

    def __setitem__(self,k,v): self.d[k] = str(v)
    def __contains__(self,k): return k in self.d

    def create_config(self):
        self.d = {'datasets_path':    str(self.config_path/'datasets'),
                  'models_path':      str(self.config_path/'models')}

        try:
            self.d["libdata_path"] = str(Path(__file__).parent/"data")
        except NameError:
            self.d["libdata_path"] = str(Path(os.getcwd())/"frenchtext"/"data")

# Cell
config = Config()

# Cell
import requests
from fastprogress.fastprogress import progress_bar,master_bar

# Cell
def download_url(url, dest, file_size=0, overwrite=False, pbar=None, show_progress=True, chunk_size=1024*1024,
                 timeout=10, retries=3):
    "Download `url` to `dest` unless it exists and not `overwrite`"
    if os.path.exists(dest) and not overwrite: return

    s = requests.Session()
    s.mount('http://',requests.adapters.HTTPAdapter(max_retries=retries))
    # additional line to identify as a firefox browser, see fastai/#2438
    s.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'})
    u = s.get(url, stream=True, timeout=timeout)
    if file_size==0:
        try: file_size = int(u.headers["Content-Length"])
        except: show_progress = False

    with open(dest, 'wb') as f:
        nbytes = 0
        if show_progress:
            pbar = progress_bar(range(file_size), leave=False, parent=pbar)
            pbar.comment = dest.name
        try:
            if show_progress: pbar.update(0)
            for chunk in u.iter_content(chunk_size=chunk_size):
                nbytes += len(chunk)
                if show_progress: pbar.update(nbytes)
                f.write(chunk)
        except requests.exceptions.ConnectionError as e:
            fname = url.split('/')[-1]
            data_dir = dest.parent
            print(f'\n Download of {url} has failed after {retries} retries\n'
                  f' Fix the download manually:\n'
                  f'$ mkdir -p {data_dir}\n'
                  f'$ cd {data_dir}\n'
                  f'$ wget -c {url}\n'
                  f'$ tar xf {fname}\n'
                  f' And re-run your code once the download is successful\n')
            return

    if dest.name.endswith(".zip"):
        file = ZipFile(dest, compression=ZIP_LZMA)
        print(f"Extracting {dest.name} (this may last several seconds) ...")
        file.extractall(dest.parent)
        file.close()
        os.remove(dest)
        print("OK")
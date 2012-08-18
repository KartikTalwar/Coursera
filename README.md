## Coursera Lectures Downloader

### Dependencies:

- Python 2.7
- Mechanize
- BeautifulSoup

These dependencies can be installed easily via `pip` 

```sh
$ pip install mechanize
$ pip install BeautifulSoup
```

### Usage

Simply run `coursera.py` via python and you will be asked to enter in your details.
The files will be downloaded in the same directory where `coursera.py` is.

```sh
$ python coursera.py
```

```
  Username: (enter your email address here)
  Passowrd: (enter your coursera password)
  Course  : (enter the code of the course) [eg: nlp, algo, crypto, qcomp-2012-001]
```

**Course**


The course code, which is the 3rd input required by the user can be found in the URL of the course page

###### Example

Quantum Mechanics and Quantum Computing

https://class.coursera.org/qcomp-2012-001/class/index

The course code here is *qcomp-2012-001*


### Features and Bugs

- More features are under their way but feel free to create a feature or a bug issue

### License

- TBD

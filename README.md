# SeleniumScraper

Use SeleniumScraper if you need a dataset of images.

This scraper can download images from Google Image, Imgur, and Pexel.  

SeleniumScraper is compatible with: __Python 2.7-3.7__.

This module will **not** work to scrap any underage content.

## Getting started in 30 seconds.

```python
from selenium_scraper import SeleniumScraper

scraper = SeleniumScraper()

categories = ['Rose flower', 'Tulip flower']

nb = scraper.begin_scrap(categories)
```

## Some options.

```python
from selenium_scraper import SeleniumScraper

scraper2 = SeleniumScraper(driver="Firefox", dest="img", quality="max", limit=50, pexel=True, imgur=True)

nb__img_example_2 = scraper2.begin_scrap("Dandelion")
```

------------------
- `driver` supported :
```python
driver="Chromium"  # default -- use Chrome headless
driver="Chrome"
driver="Firefox"
driver="PhantomJS"
```
------------------
- `dest` : path destination
```python
dest="."  # default
```
------------------
- `quality` : quality of image's downloaded
```python
dest="min"  # default
dest="max"
```
------------------
- `limit` : limit of images to download for each website activated
```python
limit=0  # default -- 0 means unlimited (by the website)
```
------------------
- `google` : path destination
```python
google=True  # default
google=False
```
------------------
- `pexel` : path destination
```python
pexel=True  # default
pexel=False
```
------------------
- `imgur` : path destination
```python
imgur=True  # default
imgur=False
```
------------------

## Licence

The information contained in this repository is for general information purposes only. The information is provided by Le Jeune Vincent and while I endeavour to keep the information up to date and correct, I make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability or availability with respect to the website or the information, products, services, or related graphics contained on this repository for any purpose. Any reliance you place on such information is therefore strictly at your own risk.
In no event will I be liable for any loss or damage including without limitation, indirect or consequential loss or damage, or any loss or damage whatsoever arising from loss of data or profits arising out of, or in connection with, the use of this website.
Through this website you are able to link to other websites which are not under the control of Le Jeune Vincent. I have no control over the nature, content and availability of those sites. The inclusion of any links does not necessarily imply a recommendation or endorse the views expressed within them.
Every effort is made to keep the repository up and running smoothly. However, Le Jeune Vincent takes no responsibility for, and will not be liable for, the repository being temporarily unavailable due to technical issues beyond our control.

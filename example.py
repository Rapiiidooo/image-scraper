from selenium_scraper import SeleniumScraper


def main():
    scraper = SeleniumScraper()
    categories = ['Rose flower', 'Tulip flower']
    nb_img_example = scraper.begin_scrap(categories)

    scraper2 = SeleniumScraper(driver="Firefox", dest="img", quality="max", limit=50, pexel=True, imgur=True)
    nb__img_example_2 = scraper2.begin_scrap("Dandelion")

    print(nb_img_example, " img scraped.")
    print(nb__img_example_2, " img scraped.")


if __name__ == "__main__":
    main()

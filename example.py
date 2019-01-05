from selenium_scraper import SeleniumScraper


def main():
    # scraper = SeleniumScraper(dest="img", limit=50, pexel=True, imgur=True)
	scraper = SeleniumScraper()

    categories = ['Rose flower', 'Tulip flower']

    nb_img_example = scraper.begin_scrap(categories)
    nb__img_example_2 = scraper.begin_scrap("Dandelion")

    print(nb_img_example, " img scraped.")
    print(nb__img_example_2, " img scraped.")


if __name__ == "__main__":
    main()

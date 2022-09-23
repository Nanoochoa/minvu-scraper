import argparse
from minvu_scraper import scrape_year

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape MINVU D.S.01 beneficiaries')
    parser.add_argument('-y','--year', type=int, help='year to be scraped', required=True)
    parser.add_argument('-f', '--filename', help='CSV filename to write output', required=True)
    args = parser.parse_args()
    df = scrape_year(args.year)
    df.to_csv(args.filename)
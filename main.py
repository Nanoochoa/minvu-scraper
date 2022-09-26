import argparse
from minvu_scraper import scrape_year

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape MINVU D.S.01 beneficiaries')
    parser.add_argument('-y','--year', type=int, help='year to scrape', required=True)
    parser.add_argument('-f', '--filename', help='filename of CSV output', required=True)
    parser.add_argument('-t', '--timeout', default=10, type=int, help='request timeout', required=False)
    args = parser.parse_args()
    df = scrape_year(args.year, timeout=args.timeout)
    df.to_csv(args.filename, index=False)
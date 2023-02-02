import os
import re
import sys


def process_text_file(file_name):
    websites = {}

    # open the file
    with open(file_name, 'r') as f:
        data = f.read()
        entries = re.findall(r'(.*?)->((?:\s*\d.*page:(?:\s*-\s*.+)+)+)', data)
        # page part: .*?page:((?:\s*-\s*.+)+)
        for entry in entries:
            query, pages_websites = entry
            query = query.strip().lower()
            pages_websites = pages_websites.strip().lower()
            page_lines = re.findall(r'(\d).+page:((?:\s*-\s*.+)+)', pages_websites)
            for page, websites_lines in page_lines:
                websites_list = re.findall(r'-\s*(.+)', websites_lines)
                for website in websites_list:
                    website = website.strip().lower()
                    website_extracted = re.fullmatch(
                        r'([-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,6}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?)\s*(.*)(?:(.+))?',
                        website)
                    if website_extracted:
                        website = website_extracted.group(1)
                    if website not in websites:
                        websites[website] = []
                    websites[website].append(
                        {'query': query, 'page': page, 'info': website_extracted.group(3) if website_extracted else ''})

    # write output to file named "output-<input_file_name>.txt"
    # create "output" dir
    if not os.path.exists('output'):
        os.makedirs('output')
    output_file = os.path.basename(file_name).replace(".txt", "") + '.txt'
    with open(os.path.join('output', output_file), 'w') as f:
        for website, queries in websites.items():
            f.write(f'{website} ->\n')
            for query in queries:
                f.write(f'  - {query["query"]} : {query["page"]}\n')


if __name__ == '__main__':
    # print error if no command line arguments are given
    if len(sys.argv) < 2:
        # call process_text_file for each text file in "input" subfolder
        for file_name in os.listdir('input'):
            if file_name.endswith('.txt'):
                process_text_file(os.path.join('input', file_name))
        sys.exit(0)


    # get input file from first mandatory command line argument
    input_file = sys.argv[1]

    process_text_file(input_file)

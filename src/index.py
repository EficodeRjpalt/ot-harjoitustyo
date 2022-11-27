import configparser
from os import getenv
from dotenv import load_dotenv
from services.csv_services import CSVTool as csvtool
from services.data_fetcher import DataFetcher
from services.paginator import Paginator
from services.formatter import Formatter
from services.json_reader import JSONReader as jreader
from services.reconstructor import Reconstructor


def main():

    config = configparser.ConfigParser()
    config.read('src/config.cfg')
    load_dotenv()
    mappings = jreader.read_json_to_dict(config['FILEPATHS']['mapping'])

    datafetch = DataFetcher(
        Paginator()
    )

    formatter = Formatter(
        datafetch
    )

    # Parse HTTP request configurations into settings
    settings = dict(config['COMMON'])
    settings['pat'] = getenv('GL_PAT')
    settings['issue'] = dict(config['ISSUE'])
    settings['comment'] = dict(config['COMMENT'])

    # Fetch data and foramt to readable dictioanries
    scope_data = datafetch.fetch_data(settings, data_type='issue')
    filtered_scope_data = formatter.format_response_data_to_dict(scope_data)

    # Transform dicts to issues
    issue_dict_list = formatter.transform_dict_items_into_issues(
        filtered_scope_data)

    ## Formatting of the issue dict list could be isolated to a separate function
    ## that aggregates all the formatting functions.
    formatter.add_comments_to_all_issues(issue_dict_list, settings)
    # Issue field names are changed from GitLab ones to Jira ones
    formatter.fix_issue_attribute_names(issue_dict_list, mappings)

    # Reconstruct the issue dict list to have Labels deconstructed
    recon_issue_dict_list = Reconstructor.reconstruct_issue_dict_attribute(
        mappings,
        issue_dict_list,
        'Labels'
    )

    # Write as a CSV with pandas
    csvtool.write_issues_to_csv(recon_issue_dict_list, 'pandas_output.csv', mappings)


if __name__ == "__main__":
    main()

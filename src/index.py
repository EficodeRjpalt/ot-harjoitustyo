import configparser
from services.csv_services import CSVTool as csvtool
from services.data_fetcher import DataFetcher
from services.paginator import Paginator
from services.formatter import Formatter
from services.reconstructor import Reconstructor
from services.settings_getter import SettingsGetter


def main():

    datafetch = DataFetcher(
        Paginator()
    )

    formatter = Formatter(
        datafetch
    )

    # Get settings for http requests, column header mappings and
    # deconstructable attributes' list
    settings_getter = SettingsGetter(
        'src/config.cfg',
        configparser.ConfigParser()
    )

    http_settings = settings_getter.get_http_request_settings()
    mappings = settings_getter.get_header_mappings()
    deconst_attrs = settings_getter.get_deconstruction_attributes()

    # Fetch data from GitLab API
    scope_data = datafetch.fetch_data(http_settings, data_type='issue')

    # Format the fetched data
    issue_dict_list = formatter.format_fetched_issue_data(
        scope_data,
        http_settings,
        mappings
    )

    reconst_list = Reconstructor.reconstruct_all_issue_dict_attributes(
        mappings,
        issue_dict_list,
        deconst_attrs
    )

    csvtool.write_issues_to_csv(
        reconst_list, 'pandas_output.csv', mappings, deconst_attrs
    )


if __name__ == "__main__":
    main()

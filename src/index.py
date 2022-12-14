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
    header_mappings = settings_getter.get_header_mappings()
    deconst_attrs = settings_getter.get_deconstruction_attributes()
    csv_settings = settings_getter.get_csv_settings()
    user_mappings = settings_getter.get_user_mappings()
    label_configs = settings_getter.get_label_configs()

    # Fetch data from GitLab API
    scope_data = datafetch.fetch_data(http_settings, data_type='issue')

    # Format the fetched data
    issue_dict_list = formatter.format_fetched_issue_data(
        scope_data,
        http_settings,
        header_mappings,
        user_mappings
    )

    reconst_list = Reconstructor.reconstruct_all_issue_dict_attributes(
        header_mappings,
        issue_dict_list,
        deconst_attrs
    )

    csvtool.write_issues_to_csv(
        reconst_list,
        header_mappings,
        deconst_attrs,
        csv_settings,
        label_configs
    )


if __name__ == "__main__":
    main()

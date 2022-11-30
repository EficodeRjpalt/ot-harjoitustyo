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
    settings_getter = SettingsGetter('src/config.cfg')
    http_settings = settings_getter.get_http_request_settings()
    mappings = settings_getter.get_header_mappings()
    deconst_attrs = settings_getter.get_deconstruction_attributes()

    # Fetch data and foramt to readable dictioanries
    scope_data = datafetch.fetch_data(http_settings, data_type='issue')
    filtered_scope_data = formatter.format_response_data_to_dict(scope_data)

    # Transform dicts to issues
    issue_dict_list = formatter.transform_dict_items_into_issues(
        filtered_scope_data)

    # Formatting of the issue dict list could be isolated to a separate function
    # that aggregates all the formatting functions.
    formatter.add_comments_to_all_issues(issue_dict_list, http_settings)
    formatter.add_participants_to_all_issues(issue_dict_list, http_settings)
    # Issue field names are changed from GitLab ones to Jira ones
    formatter.fix_issue_attribute_names(issue_dict_list, mappings)

    reconst_list = Reconstructor.reconstruct_all_issue_dict_attributes(
        mappings,
        issue_dict_list,
        deconst_attrs
    )

    csvtool.write_issues_to_csv(
        reconst_list, 'pandas_output.csv', mappings, deconst_attrs)


if __name__ == "__main__":
    main()

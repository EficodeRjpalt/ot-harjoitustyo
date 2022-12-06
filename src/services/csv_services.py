from datetime import datetime
import pandas as pd
from pandas import DataFrame


class CSVTool():

    def __init__(self) -> None:
        pass

    @classmethod
    def write_issues_to_csv(
        cls,
        issue_list: list,
        head_mappings: dict,
        deconstr_attrs: list,
        csv_setting: dict
    ):
        """_summary_

        Args:
            issue_list (list): _description_
            out_filepath (str): _description_
            head_mappings (dict): _description_
            deconstr_attrs (list): _description_
        """

        # Turns all the issue objects into dicts
        fixed_issues = [issue.attributes for issue in issue_list]

        dataf = pd.DataFrame(data=fixed_issues, columns=head_mappings.values())

        dataf.drop(labels=deconstr_attrs, axis=1, inplace=True)

        reformatted_df = cls.reformat_deconstructed_headers(
            deconstr_attrs, dataf)

        filename = cls.construct_filename(csv_setting)

        reformatted_df.to_csv(
            filename,
            index=False
        )

        return filename

    @classmethod
    def reformat_deconstructed_headers(cls, deconst_attrs, dataf: DataFrame):
        """_summary_

        Args:
            deconst_attrs (_type_): _description_
            dataf (DataFrame): _description_

        Returns:
            _type_: _description_
        """

        rename_dict = {}

        for deconst_attr in deconst_attrs:
            cls.add_removable_elements_to_rename_dict(
                rename_dict,
                dataf,
                deconst_attr
            )

        renamed_df = dataf.rename(columns=rename_dict)

        return renamed_df

    @classmethod
    def add_removable_elements_to_rename_dict(
            cls, rename_dict: dict, dataf: DataFrame, deconst_attr: 'str'):
        """_summary_

        Args:
            rename_dict (dict): _description_
            dataf (DataFrame): _description_
            deconst_attr (str): _description_
        """

        fixable_headers = [header for header in list(
            dataf) if deconst_attr in header]

        for header in fixable_headers:
            rename_dict[header] = deconst_attr

    @classmethod
    def construct_filename(cls, settings: dict) -> str:
        """Function to construct a correctly formatted filename for
        the outputted CSV file. Returns a csv filename formatted as
        <Jira's project_key>_<timestmap>.csv.

        Args:
            settings (dict): Takes in the settings provided to the config.cfg
            file that has been read to a settings dictionary.

        Returns:
            str: Returns the filename as a string.
        """
        project_key = settings['project_key']
        timestamp = cls.get_timestamp_str()

        return project_key + '_' + timestamp + '.csv'

    @classmethod
    def get_timestamp_str(cls) -> str:
        """Helper function that returns in string format the current date
        and time.

        Returns:
            str: Returns date and time foramtted in the following way:
            mm-dd-YYYY-HH:MM:SS.
        """

        now = datetime.now()

        date = str(now.strftime('%m-%d-%Y'))
        time = str(now.strftime('%H:%M:%S'))

        return date + '-' + time

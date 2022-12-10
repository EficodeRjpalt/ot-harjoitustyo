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
        csv_setting: dict,
        label_mappings: dict
    ):

        # Turns all the issue objects into dicts
        fixed_issues = [issue.attributes for issue in issue_list]

        dataf = pd.DataFrame(data=fixed_issues, columns=head_mappings.values())

        dataf.drop(labels=deconstr_attrs, axis=1, inplace=True)

        cls.reformat_labels_to_fields(
            dataf, label_mappings
        )

        deconstr_df = cls.reformat_deconstructed_headers(
            deconstr_attrs, dataf)

        filename = cls.construct_filename(csv_setting)

        deconstr_df.to_csv(
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

    @classmethod
    def reformat_labels_to_fields(cls, dataf: DataFrame, label_mappings: dict) -> DataFrame:

        column_list = dataf.columns

        label_columns = []

        for value in column_list:
            if 'Label' in str(value):
                label_columns.append(str(value))

        for index, row in dataf.iterrows():
            for label_column in label_columns:
                if row[label_column] in list(label_mappings['labels'].keys()):
                    return_info = cls.get_df_field_value(
                        label_mappings, row[label_column])
                    cls.remap_field_value(
                        return_info,
                        row['Status'],
                        dataf,
                        index
                    )

    @classmethod
    def get_df_field_value(cls, label_mappings: dict, label_value: str):
        for field, label_values in label_mappings['labels'].items():
            if field == label_value:
                return (label_values['field'], label_values['value'])
            return None

    @classmethod
    def remap_field_value(
            cls,
            field_info: tuple,
            status_row_value: str,
            dataf: DataFrame,
            current_index: int):

        if field_info is None:
            return

        if not (field_info[0] == 'Status' and status_row_value == 'closed'):
            if field_info[0] == 'Status':
                dataf['Status'][current_index] = field_info[1]
            else:
                dataf.at[current_index, field_info[0]] = field_info[1]

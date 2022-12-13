from datetime import datetime
import pandas as pd
from pandas import DataFrame


class CSVTool():
    """A helper too to write issues in Python's dict format into
    a CSV file. Depends on pandas to handle the data manipulations
    and for writing the files.
    """

    @classmethod
    def write_issues_to_csv(
        cls,
        issue_list: list,
        head_mappings: dict,
        deconstr_attrs: list,
        csv_setting: dict,
        label_mappings: dict
    ) -> str:
        """The main function that takes in a list of issues as dicts and turns them
        into a csv. Runs a series of operations on the list: drops unnecessary fields,
        remaps labels into fields and values and purges serialized field names
        into a single name.

        Args:
            issue_list (list): a list containing Issues
            head_mappings (dict): List for mapping GitLab field names to Jira's
            field names.
            deconstr_attrs (list): List of attributes that need to be deconstructed.
            csv_setting (dict): A dict containing settings for csv writing.
            label_mappings (dict): A dictionary containing configurations on how to
            map labels to column headers and their values.

        Returns:
            str: Returns the filename of the file in which all the data was written.
        """

        # Turns all the issue objects into dicts
        fixed_issues = [issue.attributes for issue in issue_list]

        dataf = pd.DataFrame(data=fixed_issues, columns=head_mappings.values())

        dataf.drop(labels=deconstr_attrs, axis=1, inplace=True)

        cls.reformat_labels_to_fields(
            dataf, label_mappings
        )

        deconstr_df = cls.reformat_deconstructed_headers(
            deconstr_attrs, dataf
        )

        filename = cls.construct_filename(csv_setting)

        deconstr_df.to_csv(
            filename,
            index=False
        )

        return filename

    @classmethod
    def reformat_deconstructed_headers(cls, deconst_attrs: list, dataf: DataFrame) -> DataFrame:
        """Function for renaming fieldnames that have been deconstructed. E.g. if a field
        contained multiple values, it has been deconstructed into multiple columns each
        containig a single value. The columns have serialized names (Labels1, Labels2 ...),
        which need to be reformatted back to each having the same name (Labels, Labels ...).
        Iterates over the DataFrame one deconstructable attribute at a time.

        Args:
            deconst_attrs (list): A list of all the fields that were configured to be
            deconstructed. Possible values are Comments, Labels and Watchers. Values
            Strings.
            dataf (DataFrame): The current DataFrame that is being manipulated
            at the moment.

        Returns:
            DataFrame: Returns a new DataFrame that has the column headers remapped.
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
        """A helper function that iterates over all of the headers in the
        DataFrame passed in the arguments and collects the names of all the
        headers that need to be reformatted.
        Iterates over

        Args:
            rename_dict (dict): Takes in an empty dictionary to collect all
            the k-v pairs of column headers that need to be renamed (key)
            and assigns the new name as the value.
            dataf (DataFrame): The DataFrame that is currently being
            manipulated.
            deconst_attr (str): The deconstruction attribute that is currently
            being iterated over.
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
    def reformat_labels_to_fields(cls, dataf: DataFrame, label_mappings: dict) -> None:
        """Function to convert label information into field-value pairs for Jira fields.
        Collects all the columns with header name having 'Label' in it and compares the value
        in that column to the label mappings configurations provided as a dictionary. Iterates
        over the whole DataFrame to convert all the mapped labels into appropriate cell values
        in the correct columns.

        Args:
            dataf (DataFrame): The DataFrame that is currently being worked on.
            label_mappings (dict): A dictionary containing the information how the labels
            should be mapped into column headers and row values.

        """

        column_list = dataf.columns

        label_columns = []

        # Create a list containing the header names of all deconstructed label columns
        for value in column_list:
            if 'Label' in str(value):
                label_columns.append(str(value))

        # Iterate over every row in the dataframe
        for index, row in dataf.iterrows():
            # Iterate over all the label column header names to check if any of the
            # row's cell values match with the label names provided in the label
            # mappings.
            for label_column in label_columns:
                # If a row's cell value matches, fetch the label mapping information
                # and store it in the return_info containing a tuple of fieldname
                # and the cell value for the field.
                if row[label_column] in list(label_mappings['labels'].keys()):
                    return_info = cls.get_df_field_value(
                        label_mappings, row[label_column]
                    )
                    cls.remap_field_value(
                        return_info,
                        row['Status'],
                        dataf,
                        index
                    )

    @classmethod
    def get_df_field_value(cls, label_mappings: dict, cell_value: str) -> tuple:
        """A helper function to fetch the column header information and
        cell value information from label mapping configurations.

        Args:
            label_mappings (dict): A dictionary containing the label mapping
            configurations.
            cell_value (str): the value in a cell currently inspected.

        Returns:
            tuple: returns information containing firstly the name of the field
            which the cell value should have in the updated dataframe and secondly
            the value that should be placed into the given row's cell for that column.
        """

        return_tuple = None
        for field, label_values in label_mappings['labels'].items():
            if field == cell_value:
                return_tuple = (label_values['field'], label_values['value'])
                break

        return return_tuple

    @classmethod
    def remap_field_value(
            cls,
            field_info: tuple,
            status_row_value: str,
            dataf: DataFrame,
            current_index: int):
        """Helper function to place the remapped value into the manipulated
        dataframe.

        Args:
            field_info (tuple): Tuple containing information in which column
            and what value should be written to the currently manipulated row.
            status_row_value (str): The value for the Status column of the
            currently manipulated row.
            dataf (DataFrame): Takes the currently manipulated dataframe
            as an argument.
            current_index (int): The index of currently manipulated row.
        """

        if field_info is None:
            return

        if not (field_info[0] == 'Status' and status_row_value == 'closed'):
            if field_info[0] == 'Status':
                dataf.loc[[current_index], ['Status']] = field_info[1]
            else:
                dataf.at[current_index, field_info[0]] = field_info[1]

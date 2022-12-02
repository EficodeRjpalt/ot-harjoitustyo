import pandas as pd
from pandas import DataFrame

class CSVTool():

    def __init__(self) -> None:
        pass

    @classmethod
    def write_issues_to_csv(
        cls,
        issue_list: list,
        out_filepath: str,
        head_mappings: dict,
        deconstr_attrs: list
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

        reformatted_df.to_csv(out_filepath, index=False)

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

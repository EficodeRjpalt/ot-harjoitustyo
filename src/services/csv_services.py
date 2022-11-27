import pandas as pd


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

        # Turns all the issue objects into dicts
        fixed_issues = [issue.attributes for issue in issue_list]

        dataf = pd.DataFrame(data=fixed_issues, columns=head_mappings.values())

        dataf.drop(labels=deconstr_attrs, axis=1, inplace=True)

        dataf.to_csv(out_filepath, index=False)

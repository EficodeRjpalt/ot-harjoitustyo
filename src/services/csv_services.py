import pandas as pd


class CSVTool():

    def __init__(self) -> None:
        pass

    @classmethod
    def write_issues_to_csv(cls, issue_list: list, out_filepath: str, head_mappings: dict):

        # Set issue fields from GitLab fieldnames to Jira fieldnames as designated
        # in mapping.json.

        fixed_issues = [
            {
                jira_fieldname: issue.attributes[gl_fieldname]
                for (gl_fieldname, jira_fieldname)
                in head_mappings.items()
            }
            for issue in issue_list
        ]

        dataf = pd.DataFrame(data=fixed_issues, columns=head_mappings.values())

        dataf.to_csv(out_filepath, index=False)

class Reconstructor():

    def __init__(self):
        pass

    @classmethod
    def reconstruct_all_issue_dict_attributes(
            cls, header_mappings: dict,
            issue_dict_list: list,
            deconst_attributes: list) -> list:
        """_summary_

        Args:
            header_mappings (dict): _description_
            issue_dict_list (list): _description_
            deconst_attributes (list): _description_

        Returns:
            list: _description_
        """

        reconstruct_list = issue_dict_list.copy()

        for attribute in deconst_attributes:
            header_appendix = cls.generate_list_appendix(
                cls.get_max_count(issue_dict_list, attribute),
                attribute
            )

            cls.update_headers(header_mappings, header_appendix)

            for issue in issue_dict_list:
                tmp_issue = issue.copy()
                cls.reformat_tmp_issue(tmp_issue, attribute)
                reconstruct_list.append(tmp_issue)

        return reconstruct_list

    @classmethod
    def reformat_tmp_issue(cls, issue_dict: dict, deconst_attribute: str):
        """_summary_

        Args:
            issue_dict (dict): _description_
            deconst_attribute (str): _description_
        """

        attribute_list = issue_dict.attributes[deconst_attribute]

        if len(attribute_list) > 0:
            for i, num_attribute in enumerate(attribute_list):
                issue_dict.attributes[deconst_attribute + str(i + 1)] = cls.check_spaces_from_attribute(
                    deconst_attribute, num_attribute
                )

    @classmethod
    def get_max_count(cls, list_of_issues: list, attribue_name: str) -> int:
        """Function to count the maximum occurences of a given attribute on a single
        issuse.

        Args:
            list_of_issues (list): Takes in a list of issues that are represented as
            dictionaries.
            count_attribute (str): Information which of the issues' attribute is being counted.
            Options are 'Comments', 'Labels' or 'Participants'.

        Returns:
            int: Returns the maximum amount of attributes that a single issue in the
            list holds.
        """

        max_count = 0

        for issue in list_of_issues:
            issue_attr_list_count = len(issue.attributes[attribue_name])
            if issue_attr_list_count > max_count:
                max_count = issue_attr_list_count

        return max_count

    @classmethod
    def generate_list_appendix(cls, max_labels: int, attribute_type: str) -> list:
        """Generates a sub-lsit that can be addeed to the the main list containing
        the headers of an issue dictionary. Consists of serialized values for a given
        attribute type. For example: Label1, Label2, Label3 etc.

        Args:
            max_labels (int): Takes in an argument as an integer about how many entries
            there should be in the return list.
            attribute_type (str): The name of the attributes being enumerated. Options are:
            'Comments', 'Labels', 'Watchers'

        Returns:
            list: _description_
        """

        return [attribute_type + str(i) for i in range(1, max_labels + 1)]

    @classmethod
    def check_spaces_from_attribute(cls, check_type: str, attribute: str) -> str:
        """_summary_

        Args:
            check_type (str): _description_
            attribute (str): _description_

        Returns:
            str: _description_
        """

        if check_type == 'Labels':
            return attribute.strip().replace(' ', '_')

        return attribute

    @classmethod
    def update_headers(cls, header_mappings: dict, header_appendix: list) -> None:
        """_summary_

        Args:
            header_mappings (dict): _description_
            header_appendix (list): _description_
        """

        for appendix in header_appendix:
            header_mappings[appendix] = appendix

class Reconstructor():

    def __init__(self):
        pass

    @classmethod
    def reconstruct_issue_dict_attribute(cls, header_mappings: dict, issue_dict_list: list, deconst_attribute: str) -> tuple:

        reconstructed_issues = []

        header_appendix = cls.generate_list_appendix(
            cls.get_max_count(issue_dict_list, deconst_attribute),
            deconst_attribute
        )

        cls.update_headers(header_mappings, header_appendix)

        for issue in issue_dict_list:
            tmp_issue = issue.copy()
            attribute_list = tmp_issue.attributes[deconst_attribute]
            if len(attribute_list) > 0:
                for i, attribute in enumerate(attribute_list):
                    tmp_issue.attributes[deconst_attribute + str(i + 1)] = cls.check_spaces_from_attribute(
                        deconst_attribute, attribute)

            # Needs fixing
            #tmp_issue.attributes.pop(deconst_attribute)
            #header_mappings.pop(deconst_attribute)
            reconstructed_issues.append(tmp_issue)

        return reconstructed_issues

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
        if not cls.validate_attribute(attribue_name):
            raise TypeError('Invalid attribute name provided!')

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

        if not cls.validate_attribute(attribute_type):
            raise TypeError('Invalid attribute name provided!')

        return [attribute_type + str(i) for i in range(1, max_labels + 1)]

    @classmethod
    def validate_attribute(cls, attribute: str) -> bool:
        """Validator method to check that correct attribute names are being passed
        to Reconstructor functions.

        Args:
            attribute (str): The attributane name that needs to be tested for validation.
            Acceptable values: 'Comment', 'Label' or 'Wathcer'.

        Returns:
            bool: Function returns True if the argument attribute is on whitelisted
            list. Otherwise returns False.
        """

        valid_values = [
            'Comments',
            'Labels',
            'Watchers'
        ]

        if attribute not in valid_values:
            return False

        return True

    @classmethod
    def check_spaces_from_attribute(cls, check_type: str, attribute: str) -> str:

        if check_type == 'Labels':
            return attribute.strip().replace(' ', '_')

        return attribute

    @classmethod
    def update_headers(cls, header_mappings: dict, header_appendix: list) -> None:

        for appendix in header_appendix:
            header_mappings[appendix] = appendix

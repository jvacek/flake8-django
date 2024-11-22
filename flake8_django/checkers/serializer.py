import astroid

from .base_model_checker import BaseModelChecker
from .issue import Issue


class DJ26(Issue):
    code = "DJ26"
    description = "Do not use exclude with ModelSerializer, use fields instead"


class DJ27(Issue):
    code = "DJ27"
    description = "Do not use __all__ with ModelSerializer, use fields instead"


class SerializerChecker(BaseModelChecker):
    """
    Checker for Django REST Framework serializer patterns.
    Similar to ModelFormChecker but for DRF serializers.
    """

    model_name_lookups = [
        ".ModelSerializer",
        "rest_framework.serializers.ModelSerializer",
    ]

    def checker_applies(self, node):
        return self.is_model(node)

    def is_string_dunder_all(self, element):
        """
        Return True if element equals "__all__" in any form (string, bytes, or in list/tuple)
        """
        assign_value = element.value
        if not isinstance(assign_value, (astroid.List, astroid.Tuple, astroid.Const)):
            return False

        if isinstance(assign_value, (astroid.List, astroid.Tuple)):
            return any(
                iter_item.value == "__all__" for iter_item in assign_value.itered()
            )
        else:
            node_value = assign_value.value
            if isinstance(node_value, bytes):
                node_value = node_value.decode()
            return node_value == "__all__"

    def run(self, node):
        """
        Check for exclude and __all__ usage in ModelSerializer Meta class
        """
        if not self.checker_applies(node):
            return

        issues = []
        for body in node.body:
            if not isinstance(body, astroid.ClassDef):
                continue

            for element in body.body:
                if not isinstance(element, astroid.Assign):
                    continue

                for target in element.targets:
                    if target.name == "fields" and self.is_string_dunder_all(element):
                        issues.append(
                            DJ27(
                                lineno=node.lineno,
                                col=node.col_offset,
                            )
                        )
                    elif target.name == "exclude":
                        issues.append(
                            DJ26(
                                lineno=node.lineno,
                                col=node.col_offset,
                            )
                        )
        return issues

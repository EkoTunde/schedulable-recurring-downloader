from settings import SeleniumBy, SeleniumSelectionType, SeleniumType


def build_instruction(
    action: SeleniumType,
    by: SeleniumBy,
    value: str,
    input_text: str = None,
    selection_type: SeleniumSelectionType = None,
    select_value: str = None
) -> str:
    base = "{action} el {by} llamado {value}".format(
        action=SeleniumType.human_text(action),
        by=SeleniumBy.human_text(by),
        value=value
    )
    if action == SeleniumType.CLICK:
        return base
    elif action == SeleniumType.FILL:
        if not input_text:
            error = (
                "Si la acción es {action}, tenés que especificar input_text"
            ).format(
                action=SeleniumType.human_text(action)
            )
            raise ValueError(error)
        return base + (f" y tipear {input_text}")
    elif action == SeleniumType.SELECT:
        if not selection_type or not select_value:
            error = (
                "Si la acción es {action}, tenés que "
                "especificar selection_type y select_value"
            ).format(
                action=SeleniumType.human_text(action)
            )
            raise ValueError(error)
        return base + \
            " y seleccionar el {select_type} igual a {select_value}".format(
                select_type=SeleniumSelectionType.human_text(selection_type),
                select_value=select_value
            )
    else:
        raise ValueError(f"{action} is not a SeleniumType.")

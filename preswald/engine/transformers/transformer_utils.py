import ast
import logging
from typing import Any

from preswald.utils import (
    generate_stable_id,
)


logger = logging.getLogger(__name__)


def get_call_func_name(call_node: ast.Call) -> str | None:
    """Return the function name from a call like `slider(...)` or `preswald.slider(...)`."""
    if isinstance(call_node.func, ast.Name):
        return call_node.func.id
    elif isinstance(call_node.func, ast.Attribute):
        return call_node.func.attr
    return None

def extract_call_args(call_node: ast.Call) -> tuple[list[Any], dict[str, Any]]:
    args = []
    kwargs = {}
    for arg in call_node.args:
        if isinstance(arg, ast.Constant):
            args.append(arg.value)
        elif isinstance(arg, ast.JoinedStr):
            # fallback to unparsed string representation
            args.append(ast.unparse(arg).strip())
        else:
            args.append(ast.dump(arg))  # or handle other node types more gracefully

    for kw in call_node.keywords:
        if isinstance(kw.value, ast.Constant):
            kwargs[kw.arg] = kw.value.value
        elif isinstance(kw.value, ast.JoinedStr):
            kwargs[kw.arg] = ast.unparse(kw.value).strip()
        else:
            kwargs[kw.arg] = ast.dump(kw.value)

    return args, kwargs


def build_component_from_args(name: str, args: list, kwargs: dict) -> dict:
    """
    Reconstruct a fallback component by calling the known component function
    with the provided args and kwargs. If the function isn't found or fails,
    returns a dictionary with the type and error.
    """
    from preswald.interfaces import components

    try:
        fn = getattr(components, name, None)
        if fn is None or not callable(fn):
            raise ValueError(f"No component function found with name '{name}'")

        _preswald_component_type = getattr(fn, "_preswald_component_type", None)
        logger.info(f'[DEBUG] build_component_from_args {name=} {args=} {kwargs=} {_preswald_component_type=} {fn.__name__}')

        result = fn(*args, **kwargs)
        preswald_component = getattr(result, "_preswald_component", None)
        if preswald_component is not None:
            logger.info(f'[DEBUG] {result=} {preswald_component=}')
            return preswald_component
        logger.info(f'[DEBUG] typeof result = {type(result)}')
        return result

    except Exception as e:
        return {
            "type": name,
            "error": f"[Rebuild Error] {e!s}"
        }


def rebuild_component_from_source(
    lifted_component_src: str,
    callsite_hint: str,
    *,
    force_render: bool=False
) -> dict:
    """
    Reconstructs a UI component from its lifted AST call expression.

    This function is typically used as a fallback during runtime errors,
    allowing the system to reinvoke the component constructor based on
    its source AST expression. Render tracking is temporarily suppressed
    during reconstruction.

    Args:
        lifted_component_src: The source code of the component call.
        callsite_hint: A string used to generate a stable component ID having form
        'filename:lineno'.

    Keyword Args:
        force_render: If True, sets `shouldRender` to True on the rebuilt component.

    Returns:
        A component dictionary that can be sent to the frontend.

    Raises:
        ValueError: If the source cannot be parsed as a valid single call expression.
        Exception: If component reconstruction fails.
    """
    expr_module = ast.parse(lifted_component_src, mode="exec")
    if (
        len(expr_module.body) == 1 and
        isinstance(expr_module.body[0], ast.Expr) and
        isinstance(expr_module.body[0].value, ast.Call)
    ):
        expr_ast = expr_module.body[0].value
        name = get_call_func_name(expr_ast)
        logger.info(f'[DEBUG] about to extract call args from ast expr {name=}')
        args, kwargs = extract_call_args(expr_ast)

        kwargs["component_id"] = generate_stable_id(prefix=name, callsite_hint=callsite_hint)

        from preswald.engine.service import PreswaldService

        service = PreswaldService.get_instance()
        with service.render_tracking_suppressed():
            component = build_component_from_args(name, args, kwargs)
        if force_render:
            component['shouldRender'] = True

        logger.info(f"[DEBUG] Reconstructed component: {component=}")
        return component

    raise ValueError("Invalid lifted_component_src: unable to parse call expression.")

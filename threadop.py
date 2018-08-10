import ast
import inspect
from textwrap import dedent


class _ThreadopTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        node.decorator_list = [
            decorator for decorator in node.decorator_list
            if not isinstance(decorator, ast.Name) or decorator.id != "enable_threadop"
        ]
        self.generic_visit(node)
        return node

    def visit_BinOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, ast.BitOr):
            if not isinstance(node.right, ast.Call):
                raise RuntimeError("The RHS of a | must be a call.")

            node.right.args.insert(0, node.left)
            return node.right

        return node


def enable_threadop(fn):
    """Transform all occurrences of the right shift operator by moving
    the left-hand expression into the right first argument position of
    the right-hand expression.

    For example, it turns::

        42 | add(2) | multiply(10) | print()

    into::

        print(multiply(add(42, 2), 10))

    Limitations:

    * The right-hand side *must* be a function call.
    * Requires access to functions' source code.
    """
    transformer = _ThreadopTransformer()
    tree = transformer.visit(ast.parse(dedent(inspect.getsource(fn))))
    code = compile(tree, inspect.getfile(fn), "exec")
    scope = {}
    exec(code, fn.__globals__, scope)
    return scope[fn.__name__]


def main(request):
    """
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        Response: Any Flask-compatible response
    """

    name = request.args.get('name')
    return {"status": "success", "greeting": f"Hello, {name}!"}, 200
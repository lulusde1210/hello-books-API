from flask import jsonify, abort, make_response


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            jsonify(f"Invalid {cls.__name__} {model_id}"), 400))

    model = cls.query.get(model_id)
    if model:
        return model
    else:
        abort(make_response(
            jsonify(f"{cls.__name__} {model_id} not found"), 404))

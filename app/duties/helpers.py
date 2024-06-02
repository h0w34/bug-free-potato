from flask import abort

def get_object_or_404(model, **kwargs):
    obj = model.query.filter_by(**kwargs).first()
    if obj is None:
        abort(404, description="Object not found")
    return obj


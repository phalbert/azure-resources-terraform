import json
import pulumi

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pulumi.Output):
            # For Pulumi outputs, use all to wait for the values and return them
            all_outputs = pulumi.Output.all(obj).apply(lambda v: v)
            return all_outputs
        elif isinstance(obj, (list, tuple)):
            return [self.default(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self.default(value) for key, value in obj.items()}
        elif hasattr(obj, '__dict__'):
            return self.default(obj.__dict__)
        else:
            try:
                return json.JSONEncoder.default(self, obj)
            except TypeError:
                return str(obj)
# Minimal stub for openai used in unit tests to avoid ModuleNotFoundError
class OpenAIStub:
    def __init__(self, *args, **kwargs):
        pass


def Completion_create(*args, **kwargs):
    return {"choices": [{"text": "stubbed response"}]}


# Expose common names used in code
OpenAI = OpenAIStub
create = Completion_create

# also provide package-level attributes
api_key = None

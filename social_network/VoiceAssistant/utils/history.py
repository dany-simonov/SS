class SessionHistory:
    def __init__(self):
        self.dialog = []

    def add_message(self, role: str, message: str):
        self.dialog.append({"role": role, "message": message})

    def get_history(self):
        return self.dialog

    def clear(self):
        self.dialog = []

class Observer:
    def update(self, message):
        try:
            raise NotImplementedError("Subclass must implement abstract method")
        except Exception as ex:
            print(f"ERROR: {ex}")
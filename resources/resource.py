class Resource:

    @classmethod
    def init_from_event(cls, event, context):
        obj = cls()
        obj._event = event
        obj._context = context

        return obj

    @classmethod
    def resource_type(cls):
        return cls.__name__

    def create(self):
        print(f'{self.__class__.__name__} create')

    def update(self):
        print(f'{self.__class__.__name__} update')

    def delete(self):
        print(f'{self.__class__.__name__} delete')

    @property
    def physical_id(self):
        return self._event.get('PhysicalResourceId')

    @property
    def response_data(self):
        return {}
        

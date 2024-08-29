class Function(models.Model):
    functionid = models.UUIDField(primary_key=True, default=uuid.uuid1)  # This field type is a guess.
    name = models.TextField(blank=True, null=True)
    functiontype = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    defaultconfig = JSONField(blank=True, null=True)
    modulename = models.TextField(blank=True, null=True)
    classname = models.TextField(blank=True, null=True)
    component = models.TextField(blank=True, null=True, unique=True)

    class Meta:
        managed = True
        db_table = 'functions'

    @property
    def defaultconfig_json(self):
        json_string = json.dumps(self.defaultconfig)
        return json_string

    def get_class_module(self):
        mod_path = self.modulename.replace('.py', '')
        module = None
        import_success = False
        import_error = None
        for function_dir in settings.FUNCTION_LOCATIONS:
            try:
                module = importlib.import_module(function_dir + '.%s' % mod_path)
                import_success = True
            except ImportError as e:
                import_error = e
            if module is not None:
                break
        if import_success == False:
            print('Failed to import ' + mod_path)
            print(import_error)

        func = getattr(module, self.classname)
        return func

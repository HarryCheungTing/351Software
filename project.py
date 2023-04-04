class Project:
    def __init__(self, uid, name, description, progress, dueDate):
        self.uid = uid
        self.name = name
        self.description = description
        self.progress = progress
        self.dueDate = dueDate
        self.subprojects = []

    def update(self, uid, name, description, progress, dueDate):
        self.uid = uid
        self.name = name
        self.description = description
        self.progress = progress
        self.dueDate = dueDate
        
    def add_subproject(self, subproject):
        self.subprojects.append(subproject)
        self.update_progress()

    def remove_subproject(self, index):
        self.subprojects.pop(index)
        self.update_progress()

    def update_progress(self):
        if self.subprojects:
            total_progress = sum([subproject.progress for subproject in self.subprojects])
            self.progress = total_progress // len(self.subprojects)
        else:
            self.progress = 0

    def update_subproject(self, index, progress):
        self.subprojects[index].progress = progress
        self.update_progress()

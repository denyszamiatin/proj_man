class ProjectManagerError(Exception):
    pass


class MemberError(ProjectManagerError):
    pass

class ProjectError(ProjectManagerError):
    pass


class UserError(ProjectManagerError):
    pass


class DatabaseProjectError(ProjectManagerError):
    pass


class DatabaseUserError(ProjectManagerError):
    pass
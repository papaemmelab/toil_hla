"""toil_hla specific exceptions."""


class PackageBaseException(Exception):

    """A base exception for toil_brass."""


class ValidationError(PackageBaseException):

    """A class to raise when a validation error occurs."""

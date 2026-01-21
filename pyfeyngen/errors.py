class FeyngenError(Exception):
    """
    Base class for all pyfeyngen errors.
    """
    pass

class InvalidReactionError(FeyngenError):
    """
    Raised when the reaction string syntax is incorrect.
    """
    pass

class UnknownParticleError(FeyngenError):
    """
    Raised when a particle is not found in physics.py.
    """
    pass
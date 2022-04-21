import pickle


def packing(source_object: object) -> bytes:
    """
    A pickle function to pack the object in bytes.

    Parameters
    ----------
    source_object : object
        Any object or dataclass.

    Returns
    -------
    bytes
        Pickle object in bytes.

    """
    if source_object is None:
        return
    pickled_object = pickle.dumps(source_object)
    return pickled_object


def unpacking(pickled_object: bytes) -> object:
    """
    A function to convert any pickle bytes into its object

    Parameters
    ----------
    pickled_object : bytes
        Pickle object in bytes.

    Returns
    -------
    object
        Object or dataclass.

    """
    if pickled_object is None:
        return
    unpacked_object = pickle.loads(pickled_object)
    return unpacked_object

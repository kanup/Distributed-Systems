from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Confirmation(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class DeleteRequest(_message.Message):
    __slots__ = ["fileid"]
    FILEID_FIELD_NUMBER: _ClassVar[int]
    fileid: str
    def __init__(self, fileid: _Optional[str] = ...) -> None: ...

class DeleteResponse(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class PrimaryRequest(_message.Message):
    __slots__ = ["content", "fileid", "filename", "operation"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    FILEID_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    content: str
    fileid: str
    filename: str
    operation: str
    def __init__(self, operation: _Optional[str] = ..., fileid: _Optional[str] = ..., filename: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...

class ReadRequest(_message.Message):
    __slots__ = ["fileid"]
    FILEID_FIELD_NUMBER: _ClassVar[int]
    fileid: str
    def __init__(self, fileid: _Optional[str] = ...) -> None: ...

class ReadResponse(_message.Message):
    __slots__ = ["content", "filename", "status", "version"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    content: str
    filename: str
    status: str
    version: str
    def __init__(self, status: _Optional[str] = ..., filename: _Optional[str] = ..., content: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class RegisterRequest(_message.Message):
    __slots__ = ["ipaddress", "name"]
    IPADDRESS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ipaddress: str
    name: str
    def __init__(self, name: _Optional[str] = ..., ipaddress: _Optional[str] = ...) -> None: ...

class RegisterResponse(_message.Message):
    __slots__ = ["primary", "primary_ipaddress", "status"]
    PRIMARY_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_IPADDRESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    primary: bool
    primary_ipaddress: str
    status: str
    def __init__(self, status: _Optional[str] = ..., primary_ipaddress: _Optional[str] = ..., primary: bool = ...) -> None: ...

class ServerListRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ServerListResponse(_message.Message):
    __slots__ = ["listOfServers", "status"]
    LISTOFSERVERS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    listOfServers: _containers.RepeatedScalarFieldContainer[str]
    status: str
    def __init__(self, status: _Optional[str] = ..., listOfServers: _Optional[_Iterable[str]] = ...) -> None: ...

class WriteRequest(_message.Message):
    __slots__ = ["content", "fileid", "filename"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    FILEID_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    content: str
    fileid: str
    filename: str
    def __init__(self, filename: _Optional[str] = ..., content: _Optional[str] = ..., fileid: _Optional[str] = ...) -> None: ...

class WriteResponse(_message.Message):
    __slots__ = ["fileid", "status", "version"]
    FILEID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    fileid: str
    status: str
    version: str
    def __init__(self, status: _Optional[str] = ..., fileid: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

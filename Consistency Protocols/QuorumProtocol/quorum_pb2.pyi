from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeleteReplicaRequest(_message.Message):
    __slots__ = ["file_uuid"]
    FILE_UUID_FIELD_NUMBER: _ClassVar[int]
    file_uuid: str
    def __init__(self, file_uuid: _Optional[str] = ...) -> None: ...

class DeleteReplicaResponse(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetAllReplicasResponse(_message.Message):
    __slots__ = ["replica_list"]
    REPLICA_LIST_FIELD_NUMBER: _ClassVar[int]
    replica_list: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, replica_list: _Optional[_Iterable[str]] = ...) -> None: ...

class GetDeleteReplicasResponse(_message.Message):
    __slots__ = ["replica_list"]
    REPLICA_LIST_FIELD_NUMBER: _ClassVar[int]
    replica_list: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, replica_list: _Optional[_Iterable[str]] = ...) -> None: ...

class GetFileRequest(_message.Message):
    __slots__ = ["file_uuid"]
    FILE_UUID_FIELD_NUMBER: _ClassVar[int]
    file_uuid: str
    def __init__(self, file_uuid: _Optional[str] = ...) -> None: ...

class GetFilesResponse(_message.Message):
    __slots__ = ["file_list"]
    FILE_LIST_FIELD_NUMBER: _ClassVar[int]
    file_list: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, file_list: _Optional[_Iterable[str]] = ...) -> None: ...

class GetReadReplicasResponse(_message.Message):
    __slots__ = ["replica_list"]
    REPLICA_LIST_FIELD_NUMBER: _ClassVar[int]
    replica_list: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, replica_list: _Optional[_Iterable[str]] = ...) -> None: ...

class GetWriteReplicasResponse(_message.Message):
    __slots__ = ["replica_list"]
    REPLICA_LIST_FIELD_NUMBER: _ClassVar[int]
    replica_list: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, replica_list: _Optional[_Iterable[str]] = ...) -> None: ...

class ReadReplicaRequest(_message.Message):
    __slots__ = ["file_uuid"]
    FILE_UUID_FIELD_NUMBER: _ClassVar[int]
    file_uuid: str
    def __init__(self, file_uuid: _Optional[str] = ...) -> None: ...

class ReadReplicaResponse(_message.Message):
    __slots__ = ["file_content", "file_name", "status", "version"]
    FILE_CONTENT_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    file_content: str
    file_name: str
    status: str
    version: _timestamp_pb2.Timestamp
    def __init__(self, status: _Optional[str] = ..., file_name: _Optional[str] = ..., file_content: _Optional[str] = ..., version: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class RegisterReplicaRequest(_message.Message):
    __slots__ = ["replica_ip", "replica_port"]
    REPLICA_IP_FIELD_NUMBER: _ClassVar[int]
    REPLICA_PORT_FIELD_NUMBER: _ClassVar[int]
    replica_ip: str
    replica_port: str
    def __init__(self, replica_ip: _Optional[str] = ..., replica_port: _Optional[str] = ...) -> None: ...

class RegisterReplicaResponse(_message.Message):
    __slots__ = ["msg"]
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: str
    def __init__(self, msg: _Optional[str] = ...) -> None: ...

class WriteReplicaRequest(_message.Message):
    __slots__ = ["file_content", "file_name", "file_uuid"]
    FILE_CONTENT_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_UUID_FIELD_NUMBER: _ClassVar[int]
    file_content: str
    file_name: str
    file_uuid: str
    def __init__(self, file_uuid: _Optional[str] = ..., file_name: _Optional[str] = ..., file_content: _Optional[str] = ...) -> None: ...

class WriteReplicaResponse(_message.Message):
    __slots__ = ["file_uuid", "status", "version"]
    FILE_UUID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    file_uuid: str
    status: str
    version: _timestamp_pb2.Timestamp
    def __init__(self, status: _Optional[str] = ..., file_uuid: _Optional[str] = ..., version: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pubsub.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cpubsub.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\x16\n\x06\x63lient\x12\x0c\n\x04uuid\x18\x01 \x01(\t\"2\n\x13\x61\x64\x64ressListResponse\x12\x1b\n\taddresses\x18\x01 \x03(\x0b\x32\x08.address\"\x07\n\x05\x45mpty\"\x18\n\x08Response\x12\x0c\n\x04\x62ody\x18\x01 \x01(\t\"5\n\x07Request\x12\x0c\n\x04port\x18\x01 \x01(\t\x12\x0e\n\x06method\x18\x02 \x01(\t\x12\x0c\n\x04\x62ody\x18\x03 \x01(\t\"\xb3\x01\n\x07\x41rticle\x12\x10\n\x06sports\x18\x05 \x01(\x08H\x00\x12\x12\n\x08politics\x18\x06 \x01(\x08H\x00\x12\x11\n\x07\x66\x61shion\x18\x07 \x01(\x08H\x00\x12\x0e\n\x06\x61uthor\x18\x01 \x01(\t\x12-\n\ttimestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12\x17\n\x06\x63lient\x18\x04 \x01(\x0b\x32\x07.clientB\x06\n\x04type\"v\n\x06Server\x12\x18\n\x07members\x18\x01 \x03(\x0b\x32\x07.client\x12\x0c\n\x04name\x18\x07 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\t\x12\x11\n\tmaxclient\x18\x03 \x01(\x05\x12#\n\x11publishedArticles\x18\x04 \x03(\x0b\x32\x08.Article\"-\n\x0f\x41rticleResponse\x12\x1a\n\x08\x61rticles\x18\x01 \x03(\x0b\x32\x08.Article\"\xa9\x01\n\x0e\x41rticleRequest\x12\x0e\n\x06\x61uthor\x18\x01 \x01(\t\x12-\n\ttimestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x10\n\x06sports\x18\x04 \x01(\x08H\x00\x12\x12\n\x08politics\x18\x05 \x01(\x08H\x00\x12\x11\n\x07\x66\x61shion\x18\x06 \x01(\x08H\x00\x12\x17\n\x06\x63lient\x18\x03 \x01(\x0b\x32\x07.clientB\x06\n\x04type\"%\n\x07\x61\x64\x64ress\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\t\"D\n\x0eRegistryServer\x12\x11\n\tmaxserver\x18\x02 \x01(\x05\x12\x1f\n\ractiveServers\x18\x01 \x03(\x0b\x32\x08.addressb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'pubsub_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CLIENT._serialized_start=49
  _CLIENT._serialized_end=71
  _ADDRESSLISTRESPONSE._serialized_start=73
  _ADDRESSLISTRESPONSE._serialized_end=123
  _EMPTY._serialized_start=125
  _EMPTY._serialized_end=132
  _RESPONSE._serialized_start=134
  _RESPONSE._serialized_end=158
  _REQUEST._serialized_start=160
  _REQUEST._serialized_end=213
  _ARTICLE._serialized_start=216
  _ARTICLE._serialized_end=395
  _SERVER._serialized_start=397
  _SERVER._serialized_end=515
  _ARTICLERESPONSE._serialized_start=517
  _ARTICLERESPONSE._serialized_end=562
  _ARTICLEREQUEST._serialized_start=565
  _ARTICLEREQUEST._serialized_end=734
  _ADDRESS._serialized_start=736
  _ADDRESS._serialized_end=773
  _REGISTRYSERVER._serialized_start=775
  _REGISTRYSERVER._serialized_end=843
# @@protoc_insertion_point(module_scope)
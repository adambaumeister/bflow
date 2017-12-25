# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bflow.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='bflow.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x0b\x62\x66low.proto\"!\n\rMessageParser\x12\x10\n\x08\x66unction\x18\x01 \x01(\t\".\n\x0cGenericQuery\x12\x10\n\x08\x66unction\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\t\"1\n\x0fGenericResponse\x12\x10\n\x08\x66unction\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\t\"7\n\tAddRouter\x12\x10\n\x08\x66unction\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\"\\\n\tAddSubnet\x12\x10\n\x08\x66unction\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0e\n\x06router\x18\x03 \x01(\t\x12\x0e\n\x06subnet\x18\x04 \x01(\t\x12\x11\n\tinterface\x18\x05 \x01(\t\"{\n\rMacTableQuery\x12\x10\n\x08\x66unction\x18\x01 \x01(\t\x12\x0e\n\x06switch\x18\x02 \x01(\t\x12&\n\tQueryType\x18\x03 \x01(\x0e\x32\x13.MacTableQuery.type\" \n\x04type\x12\n\n\x06NORMAL\x10\x00\x12\x0c\n\x08\x44\x45TAILED\x10\x01\"L\n\rMacTableEntry\x12\x10\n\x08\x66unction\x18\x01 \x01(\t\x12\x0e\n\x06switch\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\t\x12\x0b\n\x03mac\x18\x04 \x01(\tb\x06proto3')
)



_MACTABLEQUERY_TYPE = _descriptor.EnumDescriptor(
  name='type',
  full_name='MacTableQuery.type',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NORMAL', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DETAILED', index=1, number=1,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=391,
  serialized_end=423,
)
_sym_db.RegisterEnumDescriptor(_MACTABLEQUERY_TYPE)


_MESSAGEPARSER = _descriptor.Descriptor(
  name='MessageParser',
  full_name='MessageParser',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='function', full_name='MessageParser.function', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=15,
  serialized_end=48,
)


_GENERICQUERY = _descriptor.Descriptor(
  name='GenericQuery',
  full_name='GenericQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='function', full_name='GenericQuery.function', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='GenericQuery.data', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=50,
  serialized_end=96,
)


_GENERICRESPONSE = _descriptor.Descriptor(
  name='GenericResponse',
  full_name='GenericResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='function', full_name='GenericResponse.function', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='GenericResponse.data', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=98,
  serialized_end=147,
)


_ADDROUTER = _descriptor.Descriptor(
  name='AddRouter',
  full_name='AddRouter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='function', full_name='AddRouter.function', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='AddRouter.id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='AddRouter.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=149,
  serialized_end=204,
)


_ADDSUBNET = _descriptor.Descriptor(
  name='AddSubnet',
  full_name='AddSubnet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='function', full_name='AddSubnet.function', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='AddSubnet.id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='router', full_name='AddSubnet.router', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='subnet', full_name='AddSubnet.subnet', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='interface', full_name='AddSubnet.interface', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=206,
  serialized_end=298,
)


_MACTABLEQUERY = _descriptor.Descriptor(
  name='MacTableQuery',
  full_name='MacTableQuery',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='function', full_name='MacTableQuery.function', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='switch', full_name='MacTableQuery.switch', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='QueryType', full_name='MacTableQuery.QueryType', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MACTABLEQUERY_TYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=300,
  serialized_end=423,
)


_MACTABLEENTRY = _descriptor.Descriptor(
  name='MacTableEntry',
  full_name='MacTableEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='function', full_name='MacTableEntry.function', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='switch', full_name='MacTableEntry.switch', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='MacTableEntry.port', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mac', full_name='MacTableEntry.mac', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=425,
  serialized_end=501,
)

_MACTABLEQUERY.fields_by_name['QueryType'].enum_type = _MACTABLEQUERY_TYPE
_MACTABLEQUERY_TYPE.containing_type = _MACTABLEQUERY
DESCRIPTOR.message_types_by_name['MessageParser'] = _MESSAGEPARSER
DESCRIPTOR.message_types_by_name['GenericQuery'] = _GENERICQUERY
DESCRIPTOR.message_types_by_name['GenericResponse'] = _GENERICRESPONSE
DESCRIPTOR.message_types_by_name['AddRouter'] = _ADDROUTER
DESCRIPTOR.message_types_by_name['AddSubnet'] = _ADDSUBNET
DESCRIPTOR.message_types_by_name['MacTableQuery'] = _MACTABLEQUERY
DESCRIPTOR.message_types_by_name['MacTableEntry'] = _MACTABLEENTRY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MessageParser = _reflection.GeneratedProtocolMessageType('MessageParser', (_message.Message,), dict(
  DESCRIPTOR = _MESSAGEPARSER,
  __module__ = 'bflow_pb2'
  # @@protoc_insertion_point(class_scope:MessageParser)
  ))
_sym_db.RegisterMessage(MessageParser)

GenericQuery = _reflection.GeneratedProtocolMessageType('GenericQuery', (_message.Message,), dict(
  DESCRIPTOR = _GENERICQUERY,
  __module__ = 'bflow_pb2'
  # @@protoc_insertion_point(class_scope:GenericQuery)
  ))
_sym_db.RegisterMessage(GenericQuery)

GenericResponse = _reflection.GeneratedProtocolMessageType('GenericResponse', (_message.Message,), dict(
  DESCRIPTOR = _GENERICRESPONSE,
  __module__ = 'bflow_pb2'
  # @@protoc_insertion_point(class_scope:GenericResponse)
  ))
_sym_db.RegisterMessage(GenericResponse)

AddRouter = _reflection.GeneratedProtocolMessageType('AddRouter', (_message.Message,), dict(
  DESCRIPTOR = _ADDROUTER,
  __module__ = 'bflow_pb2'
  # @@protoc_insertion_point(class_scope:AddRouter)
  ))
_sym_db.RegisterMessage(AddRouter)

AddSubnet = _reflection.GeneratedProtocolMessageType('AddSubnet', (_message.Message,), dict(
  DESCRIPTOR = _ADDSUBNET,
  __module__ = 'bflow_pb2'
  # @@protoc_insertion_point(class_scope:AddSubnet)
  ))
_sym_db.RegisterMessage(AddSubnet)

MacTableQuery = _reflection.GeneratedProtocolMessageType('MacTableQuery', (_message.Message,), dict(
  DESCRIPTOR = _MACTABLEQUERY,
  __module__ = 'bflow_pb2'
  # @@protoc_insertion_point(class_scope:MacTableQuery)
  ))
_sym_db.RegisterMessage(MacTableQuery)

MacTableEntry = _reflection.GeneratedProtocolMessageType('MacTableEntry', (_message.Message,), dict(
  DESCRIPTOR = _MACTABLEENTRY,
  __module__ = 'bflow_pb2'
  # @@protoc_insertion_point(class_scope:MacTableEntry)
  ))
_sym_db.RegisterMessage(MacTableEntry)


# @@protoc_insertion_point(module_scope)

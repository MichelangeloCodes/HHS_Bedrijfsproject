// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from my_interfaces:msg/Custom.idl
// generated code does not contain a copyright notice

#ifndef MY_INTERFACES__MSG__DETAIL__CUSTOM__STRUCT_H_
#define MY_INTERFACES__MSG__DETAIL__CUSTOM__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'description'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/Custom in the package my_interfaces.
typedef struct my_interfaces__msg__Custom
{
  float data;
  rosidl_runtime_c__String description;
} my_interfaces__msg__Custom;

// Struct for a sequence of my_interfaces__msg__Custom.
typedef struct my_interfaces__msg__Custom__Sequence
{
  my_interfaces__msg__Custom * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} my_interfaces__msg__Custom__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MY_INTERFACES__MSG__DETAIL__CUSTOM__STRUCT_H_

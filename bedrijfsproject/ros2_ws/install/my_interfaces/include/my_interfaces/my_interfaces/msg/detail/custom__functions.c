// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from my_interfaces:msg/Custom.idl
// generated code does not contain a copyright notice
#include "my_interfaces/msg/detail/custom__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `description`
#include "rosidl_runtime_c/string_functions.h"

bool
my_interfaces__msg__Custom__init(my_interfaces__msg__Custom * msg)
{
  if (!msg) {
    return false;
  }
  // data
  // description
  if (!rosidl_runtime_c__String__init(&msg->description)) {
    my_interfaces__msg__Custom__fini(msg);
    return false;
  }
  return true;
}

void
my_interfaces__msg__Custom__fini(my_interfaces__msg__Custom * msg)
{
  if (!msg) {
    return;
  }
  // data
  // description
  rosidl_runtime_c__String__fini(&msg->description);
}

bool
my_interfaces__msg__Custom__are_equal(const my_interfaces__msg__Custom * lhs, const my_interfaces__msg__Custom * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // data
  if (lhs->data != rhs->data) {
    return false;
  }
  // description
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->description), &(rhs->description)))
  {
    return false;
  }
  return true;
}

bool
my_interfaces__msg__Custom__copy(
  const my_interfaces__msg__Custom * input,
  my_interfaces__msg__Custom * output)
{
  if (!input || !output) {
    return false;
  }
  // data
  output->data = input->data;
  // description
  if (!rosidl_runtime_c__String__copy(
      &(input->description), &(output->description)))
  {
    return false;
  }
  return true;
}

my_interfaces__msg__Custom *
my_interfaces__msg__Custom__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  my_interfaces__msg__Custom * msg = (my_interfaces__msg__Custom *)allocator.allocate(sizeof(my_interfaces__msg__Custom), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(my_interfaces__msg__Custom));
  bool success = my_interfaces__msg__Custom__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
my_interfaces__msg__Custom__destroy(my_interfaces__msg__Custom * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    my_interfaces__msg__Custom__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
my_interfaces__msg__Custom__Sequence__init(my_interfaces__msg__Custom__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  my_interfaces__msg__Custom * data = NULL;

  if (size) {
    data = (my_interfaces__msg__Custom *)allocator.zero_allocate(size, sizeof(my_interfaces__msg__Custom), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = my_interfaces__msg__Custom__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        my_interfaces__msg__Custom__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
my_interfaces__msg__Custom__Sequence__fini(my_interfaces__msg__Custom__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      my_interfaces__msg__Custom__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

my_interfaces__msg__Custom__Sequence *
my_interfaces__msg__Custom__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  my_interfaces__msg__Custom__Sequence * array = (my_interfaces__msg__Custom__Sequence *)allocator.allocate(sizeof(my_interfaces__msg__Custom__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = my_interfaces__msg__Custom__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
my_interfaces__msg__Custom__Sequence__destroy(my_interfaces__msg__Custom__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    my_interfaces__msg__Custom__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
my_interfaces__msg__Custom__Sequence__are_equal(const my_interfaces__msg__Custom__Sequence * lhs, const my_interfaces__msg__Custom__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!my_interfaces__msg__Custom__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
my_interfaces__msg__Custom__Sequence__copy(
  const my_interfaces__msg__Custom__Sequence * input,
  my_interfaces__msg__Custom__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(my_interfaces__msg__Custom);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    my_interfaces__msg__Custom * data =
      (my_interfaces__msg__Custom *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!my_interfaces__msg__Custom__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          my_interfaces__msg__Custom__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!my_interfaces__msg__Custom__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}

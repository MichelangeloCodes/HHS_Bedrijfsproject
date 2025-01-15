// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from my_interfaces:msg/Custom.idl
// generated code does not contain a copyright notice

#ifndef MY_INTERFACES__MSG__DETAIL__CUSTOM__STRUCT_HPP_
#define MY_INTERFACES__MSG__DETAIL__CUSTOM__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__my_interfaces__msg__Custom __attribute__((deprecated))
#else
# define DEPRECATED__my_interfaces__msg__Custom __declspec(deprecated)
#endif

namespace my_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Custom_
{
  using Type = Custom_<ContainerAllocator>;

  explicit Custom_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->data = 0.0f;
      this->description = "";
    }
  }

  explicit Custom_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : description(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->data = 0.0f;
      this->description = "";
    }
  }

  // field types and members
  using _data_type =
    float;
  _data_type data;
  using _description_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _description_type description;

  // setters for named parameter idiom
  Type & set__data(
    const float & _arg)
  {
    this->data = _arg;
    return *this;
  }
  Type & set__description(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->description = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    my_interfaces::msg::Custom_<ContainerAllocator> *;
  using ConstRawPtr =
    const my_interfaces::msg::Custom_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<my_interfaces::msg::Custom_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<my_interfaces::msg::Custom_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      my_interfaces::msg::Custom_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<my_interfaces::msg::Custom_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      my_interfaces::msg::Custom_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<my_interfaces::msg::Custom_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<my_interfaces::msg::Custom_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<my_interfaces::msg::Custom_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__my_interfaces__msg__Custom
    std::shared_ptr<my_interfaces::msg::Custom_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__my_interfaces__msg__Custom
    std::shared_ptr<my_interfaces::msg::Custom_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Custom_ & other) const
  {
    if (this->data != other.data) {
      return false;
    }
    if (this->description != other.description) {
      return false;
    }
    return true;
  }
  bool operator!=(const Custom_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Custom_

// alias to use template instance with default allocator
using Custom =
  my_interfaces::msg::Custom_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace my_interfaces

#endif  // MY_INTERFACES__MSG__DETAIL__CUSTOM__STRUCT_HPP_

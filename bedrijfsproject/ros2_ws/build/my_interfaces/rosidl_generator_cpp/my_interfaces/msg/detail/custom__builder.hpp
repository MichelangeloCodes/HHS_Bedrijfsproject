// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_interfaces:msg/Custom.idl
// generated code does not contain a copyright notice

#ifndef MY_INTERFACES__MSG__DETAIL__CUSTOM__BUILDER_HPP_
#define MY_INTERFACES__MSG__DETAIL__CUSTOM__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_interfaces/msg/detail/custom__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_interfaces
{

namespace msg
{

namespace builder
{

class Init_Custom_description
{
public:
  explicit Init_Custom_description(::my_interfaces::msg::Custom & msg)
  : msg_(msg)
  {}
  ::my_interfaces::msg::Custom description(::my_interfaces::msg::Custom::_description_type arg)
  {
    msg_.description = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_interfaces::msg::Custom msg_;
};

class Init_Custom_data
{
public:
  Init_Custom_data()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Custom_description data(::my_interfaces::msg::Custom::_data_type arg)
  {
    msg_.data = std::move(arg);
    return Init_Custom_description(msg_);
  }

private:
  ::my_interfaces::msg::Custom msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_interfaces::msg::Custom>()
{
  return my_interfaces::msg::builder::Init_Custom_data();
}

}  // namespace my_interfaces

#endif  // MY_INTERFACES__MSG__DETAIL__CUSTOM__BUILDER_HPP_

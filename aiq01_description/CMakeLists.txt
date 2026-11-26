cmake_minimum_required(VERSION 3.5)
project(aiq01_description)

if(NOT CMAKE_CONFIGURATION_TYPES)
  if(NOT CMAKE_BUILD_TYPE OR CMAKE_BUILD_TYPE STREQUAL "")
    set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Build type" FORCE)
  endif()
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

# 仅安装库中实际存在的目录（urdf 引用 package://aiq01_description/meshes/）。
# rviz 配置由 ehr_ik_solver 提供，此处不再安装 rviz/launch/meshes_2。
install(DIRECTORY urdf meshes urdf_light
  DESTINATION share/${PROJECT_NAME}
)

ament_package()

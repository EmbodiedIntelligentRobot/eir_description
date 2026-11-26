cmake_minimum_required(VERSION 3.5)
project(ehr21g_half_description)

find_package(ament_cmake REQUIRED)

install(DIRECTORY urdf meshes rviz
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(Python3 REQUIRED COMPONENTS Interpreter)
  enable_testing()
  add_test(NAME ehr21g_simulation_structure
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/test/test_simulation_baseline.py)
endif()

ament_package()

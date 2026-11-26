cmake_minimum_required(VERSION 3.5)
project(ehr21_half_description)

find_package(ament_cmake REQUIRED)

install(DIRECTORY urdf meshes rviz
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(Python3 REQUIRED COMPONENTS Interpreter)
  enable_testing()
  add_test(NAME ehr_half_waist_closed_chain
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/test/test_waist_closed_chain.py)
  add_test(NAME ehr21_finger_actuators
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/test/test_finger_actuators.py)
endif()

ament_package()

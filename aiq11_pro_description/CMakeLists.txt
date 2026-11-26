cmake_minimum_required(VERSION 3.5)
project(aiq11_pro_description)

find_package(ament_cmake REQUIRED)

install(DIRECTORY urdf meshes rviz kinematics scenes
  DESTINATION share/${PROJECT_NAME}
)

ament_package()

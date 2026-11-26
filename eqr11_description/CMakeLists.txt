cmake_minimum_required(VERSION 3.5)
project(eqr11_description)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

find_package(ament_cmake REQUIRED)

set(_retired_collision_meshes
  "base_link_collision_closure_00.STL"
  "base_link_collision_closure_01.STL"
  "base_link_collision_closure_02.STL"
  "base_link_collision_closure_03.STL"
  "base_link_collision_fit_00.STL"
  "base_link_collision_fit_01.STL"
  "base_link_collision_fit_02.STL"
  "base_link_collision_fit_03.STL"
  "base_link_collision_fit_04.STL"
  "base_link_collision_fit_05.STL"
  "base_link_collision_fit_06.STL"
  "base_link_collision_fit_07.STL"
  "base_link_collision_fit_08.STL"
  "base_link_collision_fit_09.STL"
  "base_link_collision_fit_10.STL"
  "base_link_collision_fit_11.STL"
  "base_link_collision_fit_12.STL"
  "base_link_collision_mount_03.STL"
  "base_link_collision_mount_09.STL"
  "fl_leg_l2_collision_beam_00.STL"
  "fl_leg_l2_collision_beam_01.STL"
  "fl_leg_l2_collision_connector.STL"
  "fl_leg_l3_collision_segment_00.STL"
  "fr_leg_l2_collision_beam_00.STL"
  "fr_leg_l2_collision_beam_01.STL"
  "fr_leg_l2_collision_connector.STL"
  "fr_leg_l3_collision_segment_00.STL"
  "hl_leg_l2_collision_beam_00.STL"
  "hl_leg_l2_collision_beam_01.STL"
  "hl_leg_l2_collision_connector.STL"
  "hl_leg_l3_collision_segment_00.STL"
  "hr_leg_l2_collision_beam_00.STL"
  "hr_leg_l2_collision_beam_01.STL"
  "hr_leg_l2_collision_connector.STL"
  "hr_leg_l3_collision_segment_00.STL"
)
# Retire the previous fine collision decomposition on upgrade.
foreach(_index RANGE 0 80)
  if(_index LESS 10)
    set(_suffix "0${_index}")
  else()
    set(_suffix "${_index}")
  endif()
  list(APPEND _retired_collision_meshes "base_link_collision_clearance_${_suffix}.STL")
endforeach()
foreach(_leg fl fr hl hr)
  list(APPEND _retired_collision_meshes
    "${_leg}_leg_l1_collision_connector_clearance_00.STL"
    "${_leg}_leg_l3_collision_segment_00_clearance_00.STL")
  foreach(_index RANGE 1 3)
    list(APPEND _retired_collision_meshes "${_leg}_leg_l3_collision_segment_0${_index}.STL")
  endforeach()
  foreach(_index RANGE 0 20)
    if(_index LESS 10)
      set(_suffix "0${_index}")
    else()
      set(_suffix "${_index}")
    endif()
    list(APPEND _retired_collision_meshes "${_leg}_leg_l2_collision_clearance_${_suffix}.STL")
  endforeach()
endforeach()
list(APPEND _retired_collision_meshes
  "fl_leg_l2_collision_simple_collision_1.STL"
  "fl_leg_l3_collision_simple_00.STL"
  "fl_leg_l3_collision_simple_01.STL"
  "fl_leg_lee_collision_sole.STL"
  "fr_leg_l2_collision_simple_collision_1.STL"
  "fr_leg_l3_collision_simple_00.STL"
  "fr_leg_l3_collision_simple_01.STL"
  "fr_leg_lee_collision_sole.STL"
  "hl_leg_l2_collision_simple_collision_1.STL"
  "hl_leg_l3_collision_simple_00.STL"
  "hl_leg_l3_collision_simple_01.STL"
  "hl_leg_lee_collision_sole.STL"
  "hr_leg_l2_collision_simple_collision_1.STL"
  "hr_leg_l3_collision_simple_00.STL"
  "hr_leg_l3_collision_simple_01.STL"
  "hr_leg_lee_collision_sole.STL"
)
foreach(_mesh IN LISTS _retired_collision_meshes)
  install(CODE "
    set(_mesh_dir \"\$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}/share/${PROJECT_NAME}/meshes\")
    if(NOT IS_SYMLINK \"\${_mesh_dir}\" AND
       NOT IS_SYMLINK \"\$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}/share/${PROJECT_NAME}\")
      file(REMOVE \"\${_mesh_dir}/${_mesh}\")
    endif()
  ")
endforeach()

install(
  DIRECTORY urdf meshes
  DESTINATION share/${PROJECT_NAME}
)

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/eqr11_description.rviz")
  install(
    FILES eqr11_description.rviz
    DESTINATION share/${PROJECT_NAME}
  )
endif()

ament_package()

cmake_minimum_required(VERSION 3.5)
project(eqr11w_description)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

find_package(ament_cmake REQUIRED)

set(_retired_stl_links base_link lidar_l1 lidar_l2
  gemini_335le_l1 gemini_335le_l2 gemini_336_l1 gemini_336_l2)
foreach(_leg fl fr hl hr)
  foreach(_link l1 l2 l3)
    list(APPEND _retired_stl_links "${_leg}_leg_${_link}")
  endforeach()
endforeach()
set(_retired_meshes)
foreach(_link IN LISTS _retired_stl_links)
  foreach(_suffix ".STL" "_simplified.STL" "_convex.STL")
    list(APPEND _retired_meshes "${_link}${_suffix}")
  endforeach()
endforeach()
foreach(_leg fl fr hl hr)
  list(APPEND _retired_meshes "${_leg}_foot_l0_collision.STL"
    "${_leg}_wheel_l0_collision.STL")
  foreach(_link foot_l0 wheel_l0)
    list(APPEND _retired_meshes "${_leg}_${_link}.STL"
      "${_leg}_${_link}_simplified.STL")
  endforeach()
  foreach(_link l4 lee)
    list(APPEND _retired_meshes "${_leg}_leg_${_link}_simplified.STL"
      "${_leg}_leg_${_link}_convex.STL")
  endforeach()
endforeach()
set(_former_visuals)
foreach(_color dark glass motor panel red shell silver white)
  list(APPEND _former_visuals "base_link_vis_${_color}")
endforeach()
foreach(_sensor lidar_l1 lidar_l2 gemini_335le_l1 gemini_335le_l2 gemini_336_l1 gemini_336_l2)
  list(APPEND _former_visuals "${_sensor}_simplified")
endforeach()
foreach(_leg fl fr hl hr)
  foreach(_part leg_l1_simplified leg_l2_vis_motor leg_l2_vis_shell leg_l3_simplified
      foot_l0_simplified wheel_l0_vis_dark wheel_l0_vis_rubber wheel_l0_vis_silver)
    list(APPEND _former_visuals "${_leg}_${_part}")
  endforeach()
endforeach()
foreach(_stem IN LISTS _former_visuals)
  list(REMOVE_ITEM _retired_meshes "${_stem}.STL")
  list(APPEND _retired_meshes "${_stem}.obj")
endforeach()
list(REMOVE_ITEM _retired_meshes
  "fl_foot_l0_collision.STL"
  "fl_wheel_l0_collision.STL"
  "fr_foot_l0_collision.STL"
  "fr_wheel_l0_collision.STL"
  "hl_foot_l0_collision.STL"
  "hl_wheel_l0_collision.STL"
  "hr_foot_l0_collision.STL"
  "hr_wheel_l0_collision.STL"
)
foreach(_mesh IN LISTS _retired_meshes)
  install(CODE "
    set(_mesh_dir \"\$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}/share/${PROJECT_NAME}/meshes\")
    if(NOT IS_SYMLINK \"\${_mesh_dir}\" AND
       NOT IS_SYMLINK \"\$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}/share/${PROJECT_NAME}\")
      file(REMOVE \"\${_mesh_dir}/${_mesh}\")
    endif()
  ")
endforeach()

set(_retired_collision_meshes
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
foreach(_index RANGE 0 78)
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
  foreach(_index RANGE 0 21)
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
  "fr_leg_l2_collision_simple_collision_1.STL"
  "fr_leg_l3_collision_simple_00.STL"
  "fr_leg_l3_collision_simple_01.STL"
  "hl_leg_l2_collision_simple_collision_1.STL"
  "hl_leg_l3_collision_simple_00.STL"
  "hl_leg_l3_collision_simple_01.STL"
  "hr_leg_l2_collision_simple_collision_1.STL"
  "hr_leg_l3_collision_simple_00.STL"
  "hr_leg_l3_collision_simple_01.STL"
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

ament_package()

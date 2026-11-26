cmake_minimum_required(VERSION 3.5)
project(eqr12_description)

find_package(ament_cmake REQUIRED)

# Remove only the retired CAD and whole-link hull assets on overlay installs.
# Directory installs otherwise leave deleted source files in an existing prefix.
set(_retired_mesh_links base_link)
foreach(_leg fl fr hl hr)
  foreach(_link l1 l2 l3 lee)
    list(APPEND _retired_mesh_links "${_leg}_leg_${_link}")
  endforeach()
endforeach()
foreach(_link IN LISTS _retired_mesh_links)
  foreach(_suffix ".STL" "_convex.STL")
    install(CODE "
      set(_mesh_dir \"\$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}/share/${PROJECT_NAME}/meshes\")
      if(NOT IS_SYMLINK \"\${_mesh_dir}\" AND
         NOT IS_SYMLINK \"\$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}/share/${PROJECT_NAME}\")
        file(REMOVE \"\${_mesh_dir}/${_link}${_suffix}\")
      endif()
    ")
  endforeach()
endforeach()

install(DIRECTORY meshes urdf
  DESTINATION share/${PROJECT_NAME}
)
install(FILES README.md
  DESTINATION share/${PROJECT_NAME}
)

ament_package()

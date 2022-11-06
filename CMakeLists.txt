cmake_minimum_required(VERSION 3.15)
project(slicot LANGUAGES Fortran C VERSION 5.8)

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

if (NOT CMAKE_BUILD_TYPE)
  message("-- No build type specified; defaulting to CMAKE_BUILD_TYPE=RelWithDebInfo.")
  set(CMAKE_BUILD_TYPE RelWithDebInfo CACHE STRING
    "Choose the type of build, options are: None Debug Release RelWithDebInfo MinSizeRel."
    FORCE)
endif (NOT CMAKE_BUILD_TYPE)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_subdirectory(src)
add_subdirectory(c_interface)
# add_subdirectory(tests)

#
# Install
#
install(
  TARGETS slicot slicot_c
  EXPORT SlicotTargets)

export(
  TARGETS slicot slicot_c
  NAMESPACE slicot:: FILE SlicotTargets.cmake
)

install(
  EXPORT      SlicotTargets
  DESTINATION "${CMAKE_INSTALL_DATADIR}/${PROJECT_NAME}/cmake"
  NAMESPACE   "${PROJECT_NAME}::"
)

configure_package_config_file(
  ${CMAKE_SOURCE_DIR}/cmake/SlicotConfig.cmake.in
  "${CMAKE_CURRENT_BINARY_DIR}/SlicotConfig.cmake"
  INSTALL_DESTINATION "${CMAKE_INSTALL_DATADIR}/${PROJECT_NAME}/cmake"
  )

install(
  FILES "${CMAKE_CURRENT_BINARY_DIR}/SlicotConfig.cmake"
  DESTINATION "${CMAKE_INSTALL_DATADIR}/slicot/cmake"
  )

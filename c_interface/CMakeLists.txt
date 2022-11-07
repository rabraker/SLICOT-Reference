# Generate header files for slicot.

# Defines ${SLICOT_SRCS}
include("${CMAKE_SOURCE_DIR}/cmake/slicot_sources.cmake")

# gfortran won't generate a prototype for subroutines which take a callback.
list(APPEND _do_not_export
  "mb02xd" "md03bd" "mb02wd" "md03ad")

file(MAKE_DIRECTORY  ${CMAKE_CURRENT_BINARY_DIR}/include/slicot)
foreach(_path_fname ${SLICOT_SOURCES})
  string(REGEX REPLACE "\/.*\/src\/" "" _src_fname ${_path_fname})
  string(REGEX REPLACE "\.f$" "" _h_name_upper ${_src_fname})
  string(TOLOWER ${_h_name_upper} _h_name )

  if(_h_name IN_LIST _do_not_export)
    continue()
  endif()

  set(_header_path ${CMAKE_CURRENT_BINARY_DIR}/include/slicot/${_h_name}.h)

  list(APPEND _install_headers ${_header_path})
  add_custom_command(
    OUTPUT ${_header_path}
    COMMAND gfortran -fc-prototypes-external -fsyntax-only ${_path_fname}
    > ${_header_path}
    DEPENDS
    ${_path_fname}
    ${CMAKE_CURRENT_BINARY_DIR}/include/slicot
    )
  add_custom_target(run_${_h_name} ALL
    DEPENDS ${_header_path})
endforeach()


add_library(slicot_c INTERFACE)
add_library(${PROJECT_NAME}::slicot_c ALIAS slicot_c)

target_link_libraries(slicot_c INTERFACE ${PROJECT_NAME}::slicot_c)
target_include_directories(slicot_c
  INTERFACE
  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
  )

install(
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/include/
    DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/"
    )

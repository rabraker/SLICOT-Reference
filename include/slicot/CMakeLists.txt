# Generate header files for slicot.

include(FortranCInterface)
FortranCInterface_HEADER(slicot_mangle.h
  MACRO_NAMESPACE "SLICOT_C_")

message(${FortranCInterface_MODULE_CASE})
include("${CMAKE_SOURCE_DIR}/cmake/slicot_sources.cmake")

list(APPEND _categories math)
foreach(category ${_categories})
  message("CATEGORY ${category}")
add_custom_command(
  OUTPUT ${CMAKE_BINARY_DIR}/include/slicot/${category}.h
  COMMAND  python3 ${CMAKE_SOURCE_DIR}/tools/generate-c-headers.py
  --category=${category} --output-dir=${CMAKE_BINARY_DIR}/include/slicot/
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
  DEPENDS ${CMAKE_SOURCE_DIR}/tools/generate-c-headers.py)
add_custom_target(run ALL
  DEPENDS ${CMAKE_BINARY_DIR}/include/slicot/${category}.h)
endforeach()
add_library(slicot_c INTERFACE)
add_library(${PROJECT_NAME}::slicot_c ALIAS slicot_c)

target_link_libraries(slicot_c INTERFACE ${PROJECT_NAME}::slicot_c)
target_include_directories(slicot_c
  INTERFACE
  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
  )

install(
  FILES ${CMAKE_BINARY_DIR}/include/slicot/slicot_mangle.h
  DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/slicot"
  )
foreach(category ${_categories})
install(
  FILES ${CMAKE_BINARY_DIR}/include/slicot/${category}.h
  DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/slicot"
  )
endforeach()

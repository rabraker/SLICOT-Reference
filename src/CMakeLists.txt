find_package(BLAS REQUIRED)
find_package(LAPACK REQUIRED)

# Defines ${SLICOT_SRCS}
include("${CMAKE_SOURCE_DIR}/cmake/slicot_sources.cmake")

set(LIBRARY_NAME "slicot")

add_library(${LIBRARY_NAME} ${SLICOT_SOURCES})
add_library(${PROJECT_NAME}::${LIBRARY_NAME} ALIAS ${LIBRARY_NAME})
target_link_libraries(${LIBRARY_NAME} PRIVATE
  ${LAPACK_LIBRABRIES}
  BLAS::BLAS
)

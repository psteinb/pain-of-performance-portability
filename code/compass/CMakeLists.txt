#include project relevant directories

CMAKE_MINIMUM_REQUIRED(VERSION 3.1)

# project name
PROJECT(compass-benchmarks CXX)
list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR})

find_package(GoogleBenchmark REQUIRED)
if(NOT ${googlebenchmark_FOUND})

  if(IS_DIRECTORY ${GOOGLEBENCHMARK_ROOT})
    message(FATAL_ERROR "GoogleBenchmark not found in ${GOOGLEBENCHMARK_ROOT}")
  else(IS_DIRECTORY ${GOOGLEBENCHMARK_ROOT})
    message(FATAL_ERROR "GoogleBenchmark not found, maybe you want to provide any custom installation path by -DGOOGLEBENCHMARK_ROOT=/path/to/library")
  endif(IS_DIRECTORY ${GOOGLEBENCHMARK_ROOT})

else()
  #include_directories(${googlebenchmark_INCLUDE_DIR})
  message(">> GoogleBenchmark found, ${googlebenchmark_INCLUDE_DIR} ${googlebenchmark_LIBRARY}")
  set(googlebenchmark_LIBRARY_DIR "")
  if(EXISTS ${googlebenchmark_LIBRARY})
    get_filename_component(googlebenchmark_LIBRARY_DIR "${googlebenchmark_LIBRARY}" DIRECTORY)
  endif()

  if(IS_DIRECTORY "${googlebenchmark_LIBRARY_DIR}")
    link_directories(${googlebenchmark_LIBRARY_DIR})
  endif()
endif()

find_package(Threads)
find_package(CpuFeatures)

add_executable(bench_sse4_available bench_sse4_available.cpp)
target_link_libraries(bench_sse4_available ${googlebenchmark_LIBRARY} ${googlebenchmark_AUX_LIBRARY} CpuFeatures::cpu_features Threads::Threads)
get_target_property(CPUFEAT_INCDIR CpuFeatures::cpu_features INTERFACE_INCLUDE_DIRECTORIES)
message("++ ${CPUFEAT_INCDIR}")
target_include_directories(bench_sse4_available PRIVATE ${googlebenchmark_INCLUDE_DIR} ${CPUFEAT_INCDIR})

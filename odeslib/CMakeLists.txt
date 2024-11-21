cmake_minimum_required(VERSION 3.26)

project(Odeslib)

set(SOURCE_FILES src/odes_lib.cpp)

add_library(odeslib SHARED ${SOURCE_FILES})

target_include_directories(odeslib PUBLIC include)

set(LIBRARY_DESTINATION "${CMAKE_SOURCE_DIR}/lib")
add_custom_command(TARGET odeslib POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:odeslib> ${LIBRARY_DESTINATION}
)

set(CMAKE_BUILD_TYPE Release
 CACHE STRING "Choose the type of build (Debug, Release, RelWithDebInfo, MinSizeRel)" FORCE)
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
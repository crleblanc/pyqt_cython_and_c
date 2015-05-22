# extremely simple Cmake project.  For more info see: http://www.cmake.org/cmake-tutorial/
cmake_minimum_required (VERSION 2.8.12)
project (CPROJECT C)
include(CheckCCompilerFlag)

# fPIC needed by Cython to create a C extension module
check_c_compiler_flag( "-fPIC" WITH_FPIC )
if( WITH_FPIC )
    add_definitions( -fPIC )
endif()

add_library(cproject cprogram.c )

install( TARGETS cproject 
         LIBRARY DESTINATION lib 
         ARCHIVE DESTINATION lib )

install( FILES cprogram.h
         DESTINATION include )

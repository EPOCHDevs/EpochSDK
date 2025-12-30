cmake_minimum_required(VERSION 3.16)

project(tree-sitter-epochscript
    VERSION 1.0.0
    DESCRIPTION "Tree-sitter grammar for EpochScript"
    LANGUAGES C
)

# Create the parser library
add_library(tree-sitter-epochscript STATIC
    src/parser.c
)

# Include directories
target_include_directories(tree-sitter-epochscript
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/bindings/c>
        $<INSTALL_INTERFACE:include>
)

# Set C standard
target_compile_features(tree-sitter-epochscript PRIVATE c_std_11)

# Compiler warnings
if(MSVC)
    target_compile_options(tree-sitter-epochscript PRIVATE /W3)
else()
    target_compile_options(tree-sitter-epochscript PRIVATE -Wall -Wextra -pedantic)
endif()

# Position independent code (for shared library linking)
set_target_properties(tree-sitter-epochscript PROPERTIES
    POSITION_INDEPENDENT_CODE ON
)

# Installation
include(GNUInstallDirs)

install(TARGETS tree-sitter-epochscript
    EXPORT tree-sitter-epochscript-targets
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

install(FILES bindings/c/tree-sitter-epochscript.h
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

# Export targets
install(EXPORT tree-sitter-epochscript-targets
    FILE tree-sitter-epochscript-targets.cmake
    NAMESPACE tree-sitter-epochscript::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/tree-sitter-epochscript
)

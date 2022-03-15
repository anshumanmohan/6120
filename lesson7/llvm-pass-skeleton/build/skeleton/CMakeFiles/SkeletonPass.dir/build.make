# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/Cellar/cmake/3.22.2/bin/cmake

# The command to remove a file.
RM = /usr/local/Cellar/cmake/3.22.2/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/anshumanmohan/Documents/6120/lesson7/llvm-pass-skeleton

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/anshumanmohan/Documents/6120/lesson7/llvm-pass-skeleton/build

# Include any dependencies generated for this target.
include skeleton/CMakeFiles/SkeletonPass.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include skeleton/CMakeFiles/SkeletonPass.dir/compiler_depend.make

# Include the progress variables for this target.
include skeleton/CMakeFiles/SkeletonPass.dir/progress.make

# Include the compile flags for this target's objects.
include skeleton/CMakeFiles/SkeletonPass.dir/flags.make

skeleton/CMakeFiles/SkeletonPass.dir/Skeleton.cpp.o: skeleton/CMakeFiles/SkeletonPass.dir/flags.make
skeleton/CMakeFiles/SkeletonPass.dir/Skeleton.cpp.o: ../skeleton/Skeleton.cpp
skeleton/CMakeFiles/SkeletonPass.dir/Skeleton.cpp.o: skeleton/CMakeFiles/SkeletonPass.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/anshumanmohan/Documents/6120/lesson7/llvm-pass-skeleton/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object skeleton/CMakeFiles/SkeletonPass.dir/Skeleton.cpp.o"
	cd /Users/anshumanmohan/Documents/6120/lesson7/llvm-pass-skeleton/build/skeleton && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT skeleton/CMakeFiles/SkeletonPass.dir/Skeleton.cpp.o -MF CMakeFiles/SkeletonPass.dir/Skeleton.cpp.o.d -o CMakeFiles/SkeletonPass.dir/Skeleton.cpp.o -c /Users/anshumanmohan/Documents/6120/lesson7/llvm-pass-skeleton/skeleton/Skeleton.cpp

skeleton/CMakeFiles/SkeletonPass.dir/Skeleton.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/SkeletonPass.dir/Skeleton.cpp.i"
	cd /Users/anshumanmohan/Documents/6120/lesson7/llvm-pass-skeleton/build/skeleton && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/anshumanmohan/Documents/6120/lesson7/llvm-pass-skeleton/skeleton/Skeleton.cpp > CMakeFiles/SkeletonPass.dir/Skeleton.cpp.i

skeleton/CMakeFiles/SkeletonPass.dir/Skeleton.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/SkeletonPass.dir/Skeleton.cpp.s"
	cd /Users/anshumanmohan/Documents/6120/lesson7/llvm-pass-skeleton/build/skeleton && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/anshumanmohan/Documents/6120/lesson7/llvm-pass-skeleton/skeleton/Skeleton.cpp -o CMakeFiles/SkeletonPass.dir/Skeleton.cpp.s

# Object files for target SkeletonPass
SkeletonPass_OBJECTS = \
"CMakeFiles/SkeletonPass.dir/Skeleton.cpp.o"

# External object files for target SkeletonPass
SkeletonPass_EXTERNAL_OBJECTS =

skeleton/libSkeletonPass.so: skeleton/CMakeFiles/SkeletonPass.dir/Skeleton.cpp.o
skeleton/libSkeletonPass.so: skeleton/CMakeFiles/SkeletonPass.dir/build.make
skeleton/libSkeletonPass.so: skeleton/CMakeFiles/SkeletonPass.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/anshumanmohan/Documents/6120/lesson7/llvm-pass-skeleton/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX shared module libSkeletonPass.so"
	cd /Users/anshumanmohan/Documents/6120/lesson7/llvm-pass-skeleton/build/skeleton && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/SkeletonPass.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
skeleton/CMakeFiles/SkeletonPass.dir/build: skeleton/libSkeletonPass.so
.PHONY : skeleton/CMakeFiles/SkeletonPass.dir/build

skeleton/CMakeFiles/SkeletonPass.dir/clean:
	cd /Users/anshumanmohan/Documents/6120/lesson7/llvm-pass-skeleton/build/skeleton && $(CMAKE_COMMAND) -P CMakeFiles/SkeletonPass.dir/cmake_clean.cmake
.PHONY : skeleton/CMakeFiles/SkeletonPass.dir/clean

skeleton/CMakeFiles/SkeletonPass.dir/depend:
	cd /Users/anshumanmohan/Documents/6120/lesson7/llvm-pass-skeleton/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/anshumanmohan/Documents/6120/lesson7/llvm-pass-skeleton /Users/anshumanmohan/Documents/6120/lesson7/llvm-pass-skeleton/skeleton /Users/anshumanmohan/Documents/6120/lesson7/llvm-pass-skeleton/build /Users/anshumanmohan/Documents/6120/lesson7/llvm-pass-skeleton/build/skeleton /Users/anshumanmohan/Documents/6120/lesson7/llvm-pass-skeleton/build/skeleton/CMakeFiles/SkeletonPass.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : skeleton/CMakeFiles/SkeletonPass.dir/depend


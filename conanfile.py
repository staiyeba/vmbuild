import os
from conans import ConanFile, python_requires, CMake

conan_tools = python_requires("conan-tools/[>=1.0.0]@includeos/stable")

class VmbuildConan(ConanFile):
    settings= "os_build","arch_build"
    name = "vmbuild"
    license = 'Apache-2.0'
    description = 'Utilities to build IncludeOS VMs'
    version = conan_tools.git_get_semver()
    generators = 'cmake'
    url = "http://github.com/includeos/vmbuild"

    scm = {
        "type" : "git",
        "url" : "auto",
        "subfolder": ".",
        "revision" : "auto"
    }

    no_copy_source=True
    default_user="includeos"
    default_channel="test"

    def build_requirements(self):
        self.build_requires("GSL/2.0.0@includeos/stable")

    def _cmake_configure(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self.source_folder)
        return cmake

    def build(self):
        cmake=self._cmake_configure()
        cmake.build()

    def package(self):
        cmake=self._cmake_configure()
        cmake.install()

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))

    def deploy(self):
        self.copy("*",dst="bin",src="bin")

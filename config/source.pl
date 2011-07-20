# These directories are created by install_mip
mipdir     => '/usr/local/mip',
moduledir  => '/usr/local/mip/modules',
configdir  => '/usr/local/mip/config',

# Packages are ordered in terms of priority
#     left - lowest priority
#     right - highest priority
pkgs       => ['gram5.ceres.auckland.ac.nz',],

# Default producer to use
producer   => 'glue',

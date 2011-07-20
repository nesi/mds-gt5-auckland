# The site package is used by site administrators
# to override or change needed information
# This package is optional, but is provided for the
# convenience of the site administrator

clusterlist => ['grow-itb'],

uids =>  { 	Site             => [ "GROW", ],
				SubCluster       => [ "scuid", ],
				Cluster          => [ "clusteruid", ],
				ComputingElement => [ "ceuid", ],
				StorageElement   => [ "seuid", ],
			}
			
